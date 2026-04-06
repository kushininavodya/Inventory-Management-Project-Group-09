import tkinter as tk
from tkinter import messagebox, ttk
from brain.stock_rules import add_or_update_item, find_item_by_name

class StockWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        colors = controller.colors
        
        # --- Responsive Main Container ---
        # Main window background
        self.configure(bg="#f0f2f5")

        # --- Top Header ---
        # Title bar
        header_frame = tk.Frame(self, bg="white", height=80)
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="📦 Inventory Management", font=("Arial", 22, "bold"), 
                 bg="white", fg=colors["primary"]).pack(pady=20)
        
        # --- Central Card Area ---
        # This frame holds the main content and expands to fill the screen
        content_frame = tk.Frame(self, bg="#f0f2f5")
        content_frame.pack(fill="both", expand=True, padx=20)

        # The Input Card
        # It will stay centered and grow with the window
        card_frame = tk.Frame(content_frame, bg="white", bd=0, highlightthickness=1, highlightbackground="#dcdde1")
        card_frame.pack(pady=10, padx=10, fill="both", expand=True)

        tk.Label(card_frame, text="ITEM DETAILS", font=("Arial", 11, "bold"), 
                 bg="white", fg="#7f8c8d").pack(pady=(20, 10))

        lbl_style = {"bg": "white", "fg": "#2f3640", "font": ("Arial", 9, "bold")}
        
        def create_input_row(label_text, icon=""):
            # Each row uses fill="x" to stay responsive
            row = tk.Frame(card_frame, bg="white")
            row.pack(fill="x", padx=30, pady=8)
            
            display_text = f"{icon}  {label_text}" if icon else label_text
            tk.Label(row, text=display_text, **lbl_style).pack(anchor="w")
            
            entry_frame = tk.Frame(row, bg="#f8f9fa", bd=0, highlightthickness=1, highlightbackground="#dcdde1")
            entry_frame.pack(fill="x", pady=5)
            
            entry = tk.Entry(entry_frame, font=("Arial", 12), bg="#f8f9fa", bd=0, fg=colors["text"])
            entry.pack(fill="x", padx=10, pady=8)
            
            def on_focus_in(e):
                entry_frame.config(highlightbackground=colors["accent"], bg="white")
                entry.config(bg="white")
            def on_focus_out(e):
                entry_frame.config(highlightbackground="#dcdde1", bg="#f8f9fa")
                entry.config(bg="#f8f9fa")
                
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
            return entry

        # Responsive Input Boxes
        self.name_e = create_input_row("ITEM NAME", "🏷️")
        self.name_e.bind("<FocusOut>", self.check_existing, add="+")
        self.name_e.bind("<KeyRelease>", self.check_existing)

        self.price_e = create_input_row("PRICE PER UNIT (Rs.)", "💰")

        # Unit Selection
        unit_row = tk.Frame(card_frame, bg="white")
        unit_row.pack(fill="x", padx=30, pady=8)
        tk.Label(unit_row, text="⚖️  UNIT TYPE", **lbl_style).pack(anchor="w")
        
        self.unit_options = ["kg", "pcs", "bundle", "packet"]
        self.unit_var = tk.StringVar(self)
        self.unit_var.set(self.unit_options[0])
        self.unit_menu = tk.OptionMenu(unit_row, self.unit_var, *self.unit_options)
        self.unit_menu.config(font=("Arial", 11), bg="#f8f9fa", relief="flat", bd=0, highlightthickness=1, highlightbackground="#dcdde1")
        self.unit_menu.pack(fill="x", pady=5, ipady=5)

        self.stock_e = create_input_row("TOTAL STOCK AMOUNT", "📈")

        # Status Message Banner
        self.status_lbl = tk.Label(card_frame, text="Ready to add new item", 
                                   bg="#f9f9f9", fg="#95a5a6", font=("Arial", 10, "italic"), height=2)
        self.status_lbl.pack(fill="x", padx=30, pady=10)

        # Centered Buttons
        btn_frame = tk.Frame(card_frame, bg="white")
        btn_frame.pack(pady=(10, 20), fill="x")

        tk.Button(btn_frame, text="💾  SAVE TO INVENTORY", bg=colors["accent"], fg="white", 
                  font=("Arial", 12, "bold"), bd=0, width=25, cursor="hand2",
                  command=self.save).pack(ipady=10, padx=50, fill="x")

        tk.Button(btn_frame, text="📋  VIEW FULL LIST", bg="#3498db", fg="white", 
                  font=("Arial", 12, "bold"), bd=0, width=25, cursor="hand2",
                  command=lambda: controller.show_frame("HistoryWindow")).pack(ipady=10, pady=(10, 0), padx=50, fill="x")
        
        # Back Button
        tk.Button(self, text="← Back to Main Dashboard", bg="#f0f2f5", fg="#7f8c8d", 
                  bd=0, font=("Arial", 10, "bold", "underline"), cursor="hand2",
                  command=lambda: controller.show_frame("MenuWindow")).pack(side="bottom", pady=20)

    def check_existing(self, event=None):
        name = self.name_e.get().strip()
        if not name: 
            self.status_lbl.config(text="Ready to add new item", fg="#95a5a6", bg="#f9f9f9")
            return
        item = find_item_by_name(name)
        if item:
            self.status_lbl.config(text=f"✅ Current Stock: {item['stock']} {item['unit']} | Price: Rs.{item['price']}", 
                                 fg=self.controller.colors["accent"], bg="#e8f8f0")
            if item['unit'] in self.unit_options: self.unit_var.set(item['unit'])
        else:
            self.status_lbl.config(text="✨ New Item Detected", fg="#3498db", bg="#ebf5fb")

    def save(self):
        name = self.name_e.get().strip()
        price = self.price_e.get().strip()
        unit = self.unit_var.get()
        stock = self.stock_e.get().strip()

        if not all([name, price, unit, stock]):
            messagebox.showwarning("Incomplete", "Please fill in all details.")
            return

        try:
            add_or_update_item(name, float(price), unit, float(stock))
            messagebox.showinfo("Success", f"'{name}' updated successfully!")
            self.name_e.delete(0, tk.END); self.price_e.delete(0, tk.END); self.stock_e.delete(0, tk.END)
            self.unit_var.set(self.unit_options[0])
            self.status_lbl.config(text="Ready to add new item", fg="#95a5a6", bg="#f9f9f9")
        except ValueError:
            messagebox.showerror("Error", "Price and Stock must be numbers.")