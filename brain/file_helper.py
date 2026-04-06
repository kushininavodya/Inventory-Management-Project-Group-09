import json
import os

# connects python with JSON files .

def read_json(filename):
    """Read data from a JSON file in the database folder."""
    filepath = os.path.join("database", filename)
    try:
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_json(filename, data):
    """Save data into a JSON file in the database folder."""
    filepath = os.path.join("database", filename)
    if not os.path.exists("database"):
        os.makedirs("database")
    with open(filepath, "w") as file:
        json.dump(data, file, indent=4)