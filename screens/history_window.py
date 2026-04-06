import tkinter as tk
from tkinter import ttk
from brain.file_helper import read_json

class HistoryWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        colors = controller.colors
        
        # --- Responsive Main Container ---
        self.configure(bg="#f0f2f5")

        # --- Style Configuration for Better Tables and Tabs ---
        style = ttk.Style()
        style.theme_use("clam")
        
        # Notebook (The Tab Container)
        style.configure("TNotebook", background="#f0f2f5", borderwidth=0, padding=0)
        
        # Tab Buttons Styling
        # We make the base (unselected) tabs small
        style.configure("TNotebook.Tab", 
                        font=("Arial", 9), 
                        padding=[15, 8], 
                        background="#dcdde1", 
                        foreground="#7f8c8d",
                        borderwidth=0)
        
        # Map: Selected tab turns Green and becomes Larger/Bolder
        style.map("TNotebook.Tab",
                  background=[("selected", colors["accent"]), ("active", "#ced6e0")],
                  foreground=[("selected", "white"), ("active", colors["accent"])],
                  font=[("selected", ("Arial", 11, "bold"))])

        style.configure("Treeview", 
                        background="white", 
                        foreground=colors["text"], 
                        rowheight=35, # Taller rows for readability
                        fieldbackground="white",
                        font=("Arial", 11))
        
        style.configure("Treeview.Heading", 
                        font=("Arial", 10, "bold"), 
                        background="#ecf0f1", 
                        foreground=colors["primary"])

        # --- Top Header ---
        header_frame = tk.Frame(self, bg="white", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        tk.Label(header_frame, text="📊 Reports & Inventory", font=("Arial", 22, "bold"), 
                 bg="white", fg=colors["primary"]).pack(pady=20)

        # --- Dashboard Summary Stat Cards ---
        summary_frame = tk.Frame(self, bg="#f0f2f5")
        summary_frame.pack(fill="x", padx=20, pady=10)

        # Card 1: Total Stock Value
        self.stock_card = tk.Frame(summary_frame, bg="white", bd=0, highlightthickness=1, highlightbackground="#dcdde1")
        self.stock_card.pack(side="left", expand=True, fill="both", padx=10)
        tk.Label(self.stock_card, text="TOTAL STOCK VALUE", font=("Arial", 8, "bold"), bg="white", fg="#7f8c8d").pack(pady=(15, 0))
        self.stock_val_lbl = tk.Label(self.stock_card, text="Rs. 0.00", font=("Arial", 18, "bold"), bg="white", fg=colors["secondary"])
        self.stock_val_lbl.pack(pady=(5, 15))

        # Card 2: Total Revenue
        self.rev_card = tk.Frame(summary_frame, bg="white", bd=0, highlightthickness=1, highlightbackground="#dcdde1")
        self.rev_card.pack(side="left", expand=True, fill="both", padx=10)
        tk.Label(self.rev_card, text="TOTAL REVENUE", font=("Arial", 8, "bold"), bg="white", fg="#7f8c8d").pack(pady=(15, 0))
        self.revenue_lbl = tk.Label(self.rev_card, text="Rs. 0.00", font=("Arial", 18, "bold"), bg="white", fg=colors["accent"])
        self.revenue_lbl.pack(pady=(5, 15))

        # --- Tab Control ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=25, pady=10)

        # Tab 1: Full Inventory
        self.stock_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.stock_tab, text="  📦  INVENTORY LIST  ")

        # Table Container
        stock_table_frame = tk.Frame(self.stock_tab, bg="white")
        stock_table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.stock_tree = ttk.Treeview(stock_table_frame, 
                                       columns=("Item", "Price", "Qty", "Unit", "Value"), 
                                       show="headings")
        
        columns = {"Item": 150, "Price": 100, "Qty": 80, "Unit": 80, "Value": 100}
        for col, width in columns.items():
            self.stock_tree.heading(col, text=col.upper())
            self.stock_tree.column(col, width=width, anchor="center")
        
        self.stock_tree.pack(side="left", fill="both", expand=True)
        
        stock_scroll = ttk.Scrollbar(stock_table_frame, orient="vertical", command=self.stock_tree.yview)
        stock_scroll.pack(side="right", fill="y")
        self.stock_tree.configure(yscrollcommand=stock_scroll.set)

        # Tab 2: Sales History
        self.sales_tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(self.sales_tab, text="  📜  SALES HISTORY  ")

        sales_table_frame = tk.Frame(self.sales_tab, bg="white")
        sales_table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.sales_tree = ttk.Treeview(sales_table_frame, columns=("Date", "Item", "Qty", "Total"), show="headings")
        for c in ("Date", "Item", "Qty", "Total"):
            self.sales_tree.heading(c, text=c.upper())
            self.sales_tree.column(c, width=120, anchor="center")
        
        self.sales_tree.pack(side="left", fill="both", expand=True)
        
        sales_scroll = ttk.Scrollbar(sales_table_frame, orient="vertical", command=self.sales_tree.yview)
        sales_scroll.pack(side="right", fill="y")
        self.sales_tree.configure(yscrollcommand=sales_scroll.set)

        # --- Back Navigation ---
        tk.Button(self, text="← Back to Dashboard", bg="#f0f2f5", fg="#7f8c8d", 
                  bd=0, font=("Arial", 10, "bold", "underline"), cursor="hand2",
                  command=lambda: controller.show_frame("MenuWindow")).pack(side="bottom", pady=20)

    def on_show(self):
        """Refreshes tables and stats every time the window is opened."""
        self.refresh_inventory()
        self.refresh_sales()

    def refresh_sales(self):
        for i in self.sales_tree.get_children():
            self.sales_tree.delete(i)
        sales = read_json("sales_history.json")
        grand_total = 0
        for s in reversed(sales):
            self.sales_tree.insert("", tk.END, values=(
                s.get('date', 'N/A'), s.get('item', 'N/A'), f"{s.get('weight', 0)}", f"Rs. {s.get('total', 0):.2f}"
            ))
            grand_total += s.get('total', 0)
        self.revenue_lbl.config(text=f"Rs. {grand_total:.2f}")

    def refresh_inventory(self):
        for i in self.stock_tree.get_children():
            self.stock_tree.delete(i)
        items = read_json("stock.json")
        total_value = 0
        self.stock_tree.tag_configure('low_stock', foreground='#e74c3c', font=("Arial", 11, "bold"))
        for item in items:
            name, price, qty, unit = item.get('name', 'N/A'), item.get('price', 0), item.get('stock', 0), item.get('unit', '')
            value = price * qty
            tag = 'low_stock' if qty < 5 else ''
            self.stock_tree.insert("", tk.END, values=(name, f"{price:.2f}", f"{qty}", unit, f"{value:.2f}"), tags=(tag,))
            total_value += value
        self.stock_val_lbl.config(text=f"Rs. {total_value:.2f}")