from brain.file_helper import read_json, save_json
from datetime import datetime

# Processes sale and updates .

def process_sale(item_name, weight):
    items = read_json("stock.json")
    sales = read_json("sales_history.json")
    
    for item in items:
        if item["name"].lower() == item_name.lower():
            if item["stock"] >= weight:
                total_cost = item["price"] * weight
                item["stock"] -= weight # Reduce the stock
                
                sale_record = {
                    "item": item["name"],
                    "weight": weight,
                    "total": total_cost,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                sales.append(sale_record)
                
                save_json("stock.json", items)
                save_json("sales_history.json", sales)
                return True, total_cost
            else:
                return False, "Not enough stock!"
                
    return False, "Item not found!"