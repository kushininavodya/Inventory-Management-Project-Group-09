import tkinter as tk
from tkinter import ttk, messagebox

class MenuWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        colors = controller.colors
        
        # --- 1. The Responsive Scrolling System ---
        # Matches the pattern in SignupWindow for a unified system feel
        self.canvas = tk.Canvas(self, bg="#f0f2f5", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f2f5")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Ensures the menu content stretches to fit the window width
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Enable mouse wheel support
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- 2. Fluid UI Design ---
        main_container = self.scrollable_frame

        # Top Header Bar
        header_frame = tk.Frame(main_container, bg="white", height=100)
        header_frame.pack(fill="x", pady=(0, 30))
        
        tk.Label(header_frame, text="🏪 Kothalawala Mart", font=("Arial", 26, "bold"), 
                 bg="white", fg=colors["primary"]).pack(pady=(20, 5))
        tk.Label(header_frame, text="Management Dashboard", font=("Arial", 10, "italic"), 
                 bg="white", fg="#7f8c8d").pack()

        # Central Menu Card
        card = tk.Frame(main_container, bg="white", bd=0, highlightthickness=1, highlightbackground="#dcdde1")
        card.pack(pady=10, padx=40, fill="both", expand=True)

        tk.Label(card, text="CHOOSE AN ACTION", font=("Arial", 11, "bold"), 
                 bg="white", fg="#7f8c8d").pack(pady=(30, 20))

        # Helper function to create consistent dashboard buttons
        def create_menu_btn(text, color, icon, command):
            btn = tk.Button(card, text=f"{icon}   {text}", bg=color, fg="white", 
                            font=("Arial", 12, "bold"), bd=0, width=35, 
                            cursor="hand2", command=command)
            btn.pack(pady=8, ipady=15) # Taller buttons for better touch/click feel
            return btn

        # Main Navigation Buttons
        create_menu_btn("POINT OF SALE (POS)", colors["accent"], "💰", 
                        lambda: controller.show_frame("BillingWindow"))

        create_menu_btn("STOCK MANAGEMENT", colors["secondary"], "📦", 
                        lambda: controller.show_frame("StockWindow"))

        create_menu_btn("REPORTS & HISTORY", "#3498db", "📊", 
                        lambda: controller.show_frame("HistoryWindow"))

        # Sign Out Section
        tk.Button(main_container, text="🔒 Secure Sign Out", bg="#f0f2f5", fg="#c0392b", 
                  font=("Arial", 10, "bold", "underline"), bd=0, cursor="hand2", 
                  command=lambda: controller.show_frame("LoginWindow")).pack(pady=(30, 20))


    def _on_canvas_configure(self, event):
        """Maintains responsiveness by matching frame width to window width."""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _on_mousewheel(self, event):
        """Standard vertical scroll logic."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")