from pymongo import MongoClient
from pymongo.errors import OperationFailure

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

# Define the validation rules as a dictionary
validation_rules = {
    "validator": {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["name", "age", "email"],
            "properties": {
                "name": {"bsonType": "string"},
                "age": {"bsonType": "int", "minimum": 0},
                "email": {
                    "bsonType": "string",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                },
            },
        }
    }
}

# Set the validation rules for the collection
try:
    db.command("collMod", collection.name, **validation_rules)
    print("Schema validation enabled.")
except OperationFailure as e:
    print(f"Failed to enable schema validation: {e.details['errmsg']}")

# Clean up (optional)
client.close()
