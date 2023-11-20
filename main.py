from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()

# Example JSON database file
DATABASE_FILE = "data.json"

# Define a Pydantic model for your data
class Item(BaseModel):
    name: str
    description: str = None

# Create a route to read items
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    items = read_data_from_db()
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

# Create a route to create items
@app.post("/items/")
async def create_item(item: Item):
    items = read_data_from_db()
    items.append(item.model_dump())
    write_data_to_db(items)
    return item

# Helper function to read data from the JSON database
def read_data_from_db():
    try:
        with open(DATABASE_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

# Helper function to write data to the JSON database
def write_data_to_db(data):
    with open(DATABASE_FILE, "w") as file:
        json.dump(data, file, indent=2)

# Run the application with uvicorn
# Example: uvicorn filename:app --reload
