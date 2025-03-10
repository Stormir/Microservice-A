from flask import Flask, request, jsonify

app = Flask(__name__)

# Mock database (temporary dictionary to store inventory items)
inventory = {}

@app.route('/inventory', methods=['POST'])
def add_item():
    """Add a new item to inventory or update quantity if it already exists"""
    data = request.get_json()

    # Validate input
    required_fields = ["name", "category", "quantity", "unit"]
    if not data or any(field not in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400  # Bad Request

    name = data["name"]
    category = data["category"]
    quantity = data["quantity"]
    unit = data["unit"]
    expiry_date = data.get("expiry_date", None)  # Expiry date is optional

    # Validate data types
    if not isinstance(name, str) or not isinstance(category, str) or not isinstance(unit, str):
        return jsonify({"error": "Invalid data type for name, category, or unit"}), 400

    if not isinstance(quantity, int) or quantity < 0:
        return jsonify({"error": "Quantity must be a non-negative integer"}), 400

    # If item already exists, update quantity
    if name in inventory:
        inventory[name]["quantity"] += quantity
        return jsonify({"message": "Item quantity updated", "inventory": inventory[name]}), 200  # Success

    # Otherwise, add new item
    inventory[name] = {
        "category": category,
        "quantity": quantity,
        "unit": unit,
        "expiry_date": expiry_date
    }

    return jsonify({"message": "Item added", "inventory": inventory[name]}), 201  # Created


@app.route('/inventory', methods=['GET'])
def get_item():
    """Search for an item in the inventory by full or partial name"""
    # Get the "name" parameter
    item_name = request.args.get("name")  

    if not item_name:
         # Bad Request if no name is provided
        return jsonify({"error": "Missing 'name' parameter"}), 400  

    # Find exact matches first
    if item_name in inventory:
        return jsonify(inventory[item_name]), 200

    # Search for partial matches
    matching_items = {
        name: details 
        for name, details in inventory.items() 
        if item_name.lower() in name.lower()
        }

    if matching_items:
        # Return all partial matches
        return jsonify(matching_items), 200  
    else:
        # Return 406 if not acceptable
        return jsonify({"error": "No matching items found"}), 406  

@app.route('/inventory', methods=['PUT'])
def update_item():
    """Update the quantity of an existing item"""
    data = request.get_json()

    # Validate input
    if not data or "name" not in data or "quantity" not in data:
        # Bad Request
        return jsonify({"error": "Missing required fields"}), 400  

    name = data["name"]
    quantity_change = data["quantity"]

    # Check if item exists in inventory
    if name not in inventory:
        # Not Found
        return jsonify({"error": "Item not found"}), 404  

    # Ensure valid quantity reduction
    if inventory[name]["quantity"] + quantity_change < 0:
        # Not Acceptable
        return jsonify({"error": "Cannot reduce quantity below zero"}), 406  

    # Update quantity
    inventory[name]["quantity"] += quantity_change

    # If quantity reaches 0, remove the item and return 204 
    if inventory[name]["quantity"] == 0:
        del inventory[name]
        # UPDATED ERROR
        return jsonify({"message": "Quantity zero, item removed"}), 204  
    # Success
    return jsonify({"message": "Item updated", "inventory": inventory[name]}), 200  

       
@app.route('/inventory', methods=['DELETE'])
def delete_item():
    """Delete an item from inventory"""
    data = request.get_json()

    # Validate input
    if not data or "name" not in data:
        # Bad Request
        return jsonify({"error": "Missing 'name' field"}), 400  

    name = data["name"]

    # Check if item exists in inventory
    if name not in inventory:
        # Not Found
        return jsonify({"error": "Item not found"}), 404  

    # Remove the item
    del inventory[name]

    # UPDATED ERROR
    return jsonify({"message": "Item successfully deleted"}), 204

if __name__ == '__main__':
    app.run(debug=True)
