import tkinter as tk
from tkinter import messagebox, ttk
from brain.stock_rules import find_item_by_name
from brain.bill_rules import process_sale

class BillingWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        colors = controller.colors
        self.cart_items = [] # Stroes items added to the bill before payment.

        # --- Responsive Main Container ---
        self.configure(bg="#f0f2f5")

        # --- Top Header ---
        header_frame = tk.Frame(self, bg="white", height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False) 
        
        # tk.Button(header_frame, text="🏠 MENU", font=("Arial", 10, "bold"), 
        #           bg="white", fg=colors["primary"], bd=0, cursor="hand2",
        #           activebackground="white", activeforeground=colors["accent"],
        #           command=lambda: controller.show_frame("MenuWindow")).pack(side="left", padx=25, pady=20)

        tk.Label(header_frame, text="🛒 POS Billing Counter", font=("Arial", 22, "bold"), 
                 bg="white", fg=colors["primary"]).pack(side="left", expand=True)
        
        tk.Frame(header_frame, bg="white", width=100).pack(side="right")
        
        # --- ORDER MATTERS FOR RESPONSIVENESS ---
        # To ensure the back button is always visible, we pack it and the checkout bar
        # from the bottom UP before packing the expanding center.

        # 1. Very Bottom Element
        tk.Button(self, text="← Back to Dashboard", bg="#f0f2f5", fg="#7f8c8d", 
                  bd=0, font=("Arial", 10, "bold", "underline"), cursor="hand2",
                  command=lambda: controller.show_frame("MenuWindow")).pack(side="bottom", pady=15)

        # 2. Element Above the Back Button
        checkout_bar = tk.Frame(self, bg=colors["primary"], pady=20)
        checkout_bar.pack(fill="x", side="bottom")

        total_frame = tk.Frame(checkout_bar, bg=colors["primary"])
        total_frame.pack(fill="x", padx=40)

        self.total_lbl = tk.Label(total_frame, text="TOTAL: Rs. 0.00", 
                                  font=("Arial", 22, "bold"), bg=colors["primary"], fg=colors["accent"])
        self.total_lbl.pack(side="left")

        tk.Button(total_frame, text="FINALIZE TRANSACTION", bg=colors["accent"], fg="white", 
                  font=("Arial", 12, "bold"), bd=0, width=22, cursor="hand2",
                  command=self.confirm_bill).pack(side="right", ipady=12)

        # 3. Expanding Center Content (Search Card + Table)
        content_frame = tk.Frame(self, bg="#f0f2f5")
        content_frame.pack(fill="both", expand=True, padx=20)

        # --- Search & Add Card ---
        card_frame = tk.Frame(content_frame, bg="white", bd=0, highlightthickness=1, highlightbackground="#dcdde1")
        card_frame.pack(pady=10, fill="x")

        lbl_style = {"bg": "white", "fg": "#7f8c8d", "font": ("Arial", 9, "bold")}
        ent_style = {"font": ("Arial", 13), "bd": 0, "highlightthickness": 1, 
                     "highlightbackground": "#dcdde1", "highlightcolor": colors["accent"]}

        input_row = tk.Frame(card_frame, bg="white")
        input_row.pack(padx=20, pady=15, fill="x")

        # Item Search Column
        col0 = tk.Frame(input_row, bg="white")
        col0.pack(side="left", expand=True, fill="x", padx=10)
        tk.Label(col0, text="SEARCH ITEM NAME", **lbl_style).pack(anchor="w")
        self.search_e = tk.Entry(col0, **ent_style)
        self.search_e.pack(fill="x", pady=5, ipady=8)
        self.search_e.bind("<KeyRelease>", self.update_info)

        # Qty Column
        col1 = tk.Frame(input_row, bg="white")
        col1.pack(side="left", padx=10)
        self.qty_title = tk.Label(col1, text="QTY", **lbl_style)
        self.qty_title.pack(anchor="w")
        self.qty_e = tk.Entry(col1, **ent_style, width=12, justify="center")
        self.qty_e.pack(pady=5, ipady=8)

        # Add Action Button
        tk.Button(input_row, text="ADD TO BILL", bg=colors["accent"], fg="white", 
                  font=("Arial", 10, "bold"), bd=0, width=15, cursor="hand2",
                  command=self.add_to_cart).pack(side="left", padx=10, pady=(18, 0), ipady=10)

        # Status Info Banner
        self.info_lbl = tk.Label(card_frame, text="Waiting for item name...", 
                                 fg="#95a5a6", bg="#f9f9f9", font=("Arial", 10, "italic"),
                                 height=2)
        self.info_lbl.pack(fill="x", padx=20, pady=(0, 10))

        # --- Cart List Section ---
        tk.Label(content_frame, text="Current Bill Items", font=("Arial", 11, "bold"), 
                 bg="#f0f2f5", fg="#7f8c8d").pack(anchor="w", padx=5, pady=(10, 5))

        # Table Container
        table_container = tk.Frame(content_frame, bg="white", bd=1, relief="flat")
        table_container.pack(fill="both", expand=True)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=35, font=("Arial", 11))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        columns = ("Item", "Qty", "Unit", "Price", "Total")
        self.tree = ttk.Treeview(table_container, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=100, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)

        tree_scroll = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        tree_scroll.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=tree_scroll.set)

    def update_info(self, event=None):
        name = self.search_e.get().strip()
        if not name:
            self.info_lbl.config(text="Waiting for item name...", fg="#95a5a6", bg="#f9f9f9")
            return
        item = find_item_by_name(name)
        if item:
            self.info_lbl.config(text=f"✅ {item['name']} | Price: Rs.{item['price']} | Stock: {item['stock']} {item['unit']}", 
                                 fg=self.controller.colors["accent"], bg="#e8f8f0")
            self.qty_title.config(text=f"QTY ({item['unit']})")
        else:
            self.info_lbl.config(text="❌ Item not found", fg="#e74c3c", bg="#fdf2f2")

    def add_to_cart(self):
        name, qty_str = self.search_e.get().strip(), self.qty_e.get().strip()
        if not name or not qty_str: return
        item = find_item_by_name(name)
        if not item: return
        try:
            qty = float(qty_str)
            if item['stock'] < qty:
                messagebox.showwarning("Stock Low", f"Only {item['stock']} available!")
                return
            tot = item['price'] * qty
            self.cart_items.append({"name": item['name'], "qty": qty, "total": tot})
            self.tree.insert("", tk.END, values=(item['name'], qty, item['unit'], f"{item['price']:.2f}", f"{tot:.2f}"))
            self.update_total()
            self.search_e.delete(0, tk.END); self.qty_e.delete(0, tk.END); self.search_e.focus()
        except ValueError: messagebox.showerror("Error", "Please enter a valid quantity.")

    def update_total(self):
        t = sum(i['total'] for i in self.cart_items)
        self.total_lbl.config(text=f"TOTAL: Rs. {t:.2f}")

    def confirm_bill(self):
        if not self.cart_items: 
            messagebox.showwarning("Empty", "Add items to the bill first.")
            return
        for i in self.cart_items: process_sale(i['name'], i['qty'])
        messagebox.showinfo("Success", "Transaction Completed Successfully!")
        self.cart_items = []; self.update_total()
        for i in self.tree.get_children(): self.tree.delete(i)