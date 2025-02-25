# Communication Contract
This microservice implements an inventory management system that handles CRUD operations for Inventory items via REST API. 

This section describes how to programmatically request and receive data from the inventory microservice.

# Requesting Data from the Microservice
### How to Make Requests
The inventory microservice operates as a RESTful API, meaning that programs can interact with it by sending HTTP requests. Your program can request data, add new inventory items, update existing ones, and remove items using standard HTTP methods. Your program should: 
1. Use HTTP methods such as GET, POST, PUT, and DELETE to interact with the service.
2. Format data as JSON for requests that require sending information (POST, PUT)
3. Handle responses correctly by checking status codes and parsing JSON responses.

### Adding an Item to the Inventory
Method: POST 
Endpoint: /inventory

To add a new item to the inventory, your program should send a POST request to the /inventory endpoint. The request must include a JSON object containing:

- name (string) - The name of the item.
- category (string) - The category the item belongs to.
- quantity (integer) - The number of items being added.
- unit (string) - The measurement unit for the item (e.g., "kg", "packs").
- expiry_date (optional, string) - The expiration date of the item

```python
import requests

url = "http://127.0.0.1:5000/inventory"

payload = {
    "name": "Butter",
    "quantity": 4,
    "category": "Food",
    "unit": "sticks",
    "expiry_date": None
}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Response:", response.json())

```
### Searching for an Item by Name (Full or Partial Search)
Method: GET 
Endpoint: /inventory?name=ITEM_NAME

To check if an item exists in the inventory, your program can send a GET request to /inventory?name=ITEM_NAME, passing the item name as a query parameter. A successful request will return a 200 OK response containing the item details. If the provided name is a partial match, the response will return all items containing the search term in their name. If the item does not exist, the service will return a 406 Not Acceptable response.

```python
import requests

url = "http://127.0.0.1:5000/inventory"
params = {"name": "Butter"}

response = requests.get(url, params=params)

print("Status Code:", response.status_code)
print("Response:", response.json())
```

### Updating an Item’s Quantity
Method: PUT 
Endpoint: /inventory

To modify an existing inventory item, send a PUT request to /inventory with the item name and the number to add or subtract from the current quantity. The service will return a 404 Not Found if the item does not exist. If the update is successful, the response will return a 200 OK with the updated item details. To stop negative quantities, a 406 Not Acceptable error will be returned. 


```python
url = "http://127.0.0.1:5000/inventory"
data = {"name": "Butter", "quantity": 2}  # Increase quantity by 2

response = requests.put(url, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())
```

### Deleting an Item
Method: DELETE
Endpoint: /inventory

To remove an item from the inventory, send a DELETE request to /inventory with the item's name in the request body. A successful deletion will return a 204 No Content. If the item does not exist, the service will return a 404 Not Found.

```python
url = "http://127.0.0.1:5000/inventory"
data = {"name": "Butter"}

response = requests.delete(url, json=data)
print("Status Code:", response.status_code)
if response.status_code == 204:
    print("Item deleted successfully.")
else:
    print("Response:", response.json())
```

# Receiving Data from the Microservice
### How Data is Returned

Every request returns a JSON response with an HTTP status code. This response will contain either the requested inventory data or an error message, depending on whether the request was successful. Your program must be able to:
1. Check HTTP status codes to determine success or failure. 
2. Parse JSON responses to extract useful info.
3. Handle error responses 


### Adding an Item 
(POST)
A successful POST request adds a new item or updates an existing one.
- Status Code: 201 Created (if a new item is added)
- Status Code: 200 OK (if an existing item is updated)
- Status Code: 400 Bad Request (A required field is missing or invalid.)

```json
{
    "message": "Item added",
    "inventory": {
        "category": "Food",
        "quantity": 4,
        "unit": "sticks",
        "expiry_date": null
    }
}
```

How to handle this:
```python
response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Response:", response.json())
```
### Searching for an ITEM
METHOD: GET

A GET request will return either an exact match or a list of partial matches.
- Status Code: 200 OK (if items are found)
- Status Code: 400 Bad Request (No name parameter was provided)
- Status Code: 406 Not Acceptable (No matching items were found)

Response Format:
```json
{
    "category": "Food",
    "quantity": 4,
    "unit": "sticks",
    "expiry_date": null
}
```
How to handle this: 
```python
response = requests.get(url, params={"name": "Butter"})
print("Status Code:", response.status_code)
print("Response:", response.json())
```

### Updating an Items Quantity 
METHOD: PUT

A PUT request updates an item's quantity and confirms the change.
- Status Code: 200 OK
- Status Code: 400 Bad Request (The request was missing required fields)
- Status Code: 404 Not Found (The item does not exist in inventory.)
- Status Code: 406 Not Acceptable (The update request would reduce quantity below zero.)

Response Format:
```json
{
    "message": "Item updated",
    "inventory": {
        "category": "Food",
        "quantity": 6,
        "unit": "sticks",
        "expiry_date": null
    }
}
```

How to handle this:
```python
response = requests.put(url, json=data)
print("Status Code:", response.status_code)
print("Response:", response.json())
```

### Deleting an Item
METHOD: DELETE

A DELETE request successfully removes an item.
- Status Code: 204 No Content (Item successfully deleted)

```python
response = requests.delete(url, json=data)
print("Status Code:", response.status_code)
if response.status_code != 204:
    print("Response:", response.json())
```




![image](https://github.com/user-attachments/assets/4e2af294-9cd1-44b9-8aa8-77604b403e7d)

