from brain.file_helper import read_json, save_json

# Add items and check prices .

def add_or_update_item(name, price, unit, stock):
    items = read_json("stock.json")
    found = False
    
    for item in items:
        if item["name"].lower() == name.lower():
            item["price"] = float(price)
            item["unit"] = unit
            item["stock"] = float(stock)
            found = True
            break
            
    if not found:
        items.append({
            "name": name,
            "price": float(price),
            "unit": unit,
            "stock": float(stock)
        })
        
    save_json("stock.json", items)
    return True

def find_item_by_name(name):
    items = read_json("stock.json")
    for item in items:
        if item["name"].lower() == name.lower():
            return item
    return None