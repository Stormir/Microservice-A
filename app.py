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
    item_name = request.args.get("name")  # Get the "name" parameter

    if not item_name:
        return jsonify({"error": "Missing 'name' parameter"}), 400  # Bad Request if no name is provided

    # Find exact matches first
    if item_name in inventory:
        return jsonify(inventory[item_name]), 200

    # Search for partial matches
    matching_items = {name: details for name, details in inventory.items() if item_name.lower() in name.lower()}

    if matching_items:
        return jsonify(matching_items), 200  # Return all partial matches
    else:
        return jsonify({"error": "No matching items found"}), 406  # Return 406 if not acceptable

@app.route('/inventory', methods=['PUT'])
def update_item():
    """Update the quantity of an existing item"""
    data = request.get_json()

    # Validate input
    if not data or "name" not in data or "quantity" not in data:
        return jsonify({"error": "Missing required fields"}), 400  # Bad Request

    name = data["name"]
    quantity_change = data["quantity"]

    # Check if item exists in inventory
    if name not in inventory:
        return jsonify({"error": "Item not found"}), 404  # Not Found

    # Ensure valid quantity reduction
    if inventory[name]["quantity"] + quantity_change < 0:
        return jsonify({"error": "Cannot reduce quantity below zero"}), 406  # Not Acceptable

    # Update quantity
    inventory[name]["quantity"] += quantity_change

    # If quantity reaches 0, remove the item and return 204 
    if inventory[name]["quantity"] == 0:
        del inventory[name]
        return '', 204  # (successful deletion)

    return jsonify({"message": "Item updated", "inventory": inventory[name]}), 200  # Success

       
@app.route('/inventory', methods=['DELETE'])
def delete_item():
    """Delete an item from inventory"""
    data = request.get_json()

    # Validate input
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' field"}), 400  # Bad Request

    name = data["name"]

    # Check if item exists in inventory
    if name not in inventory:
        return jsonify({"error": "Item not found"}), 404  # Not Found

    # Remove the item
    del inventory[name]

    return '', 204  # No Content (successful deletion)


if __name__ == '__main__':
    app.run(debug=True)
