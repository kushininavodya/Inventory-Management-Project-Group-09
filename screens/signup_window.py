import tkinter as tk
from tkinter import messagebox, ttk
from brain.login_rules import add_new_user

class SignupWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        colors = controller.colors
        
        # --- 1. The Responsive Scrolling System ---
        # This matches the pattern in your LoginWindow for consistent scrolling
        self.canvas = tk.Canvas(self, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="white")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Allow mouse wheel scrolling
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- 2. Fluid UI Design ---
        main_container = self.scrollable_frame

        # Header - Using accent color (Green) to differentiate from Login
        tk.Label(main_container, text="New Worker", font=("Arial", 28, "bold"), 
                 bg="white", fg=colors["accent"]).pack(pady=(60, 10))
        tk.Label(main_container, text="Register to access the mart system", font=("Arial", 11), 
                 bg="white", fg="#7f8c8d").pack(pady=(0, 40))
        
        # Centered Input Card
        card = tk.Frame(main_container, bg="white")
        card.pack(pady=10, padx=40, fill="x")

        lbl_style = {"bg": "white", "fg": "#2f3640", "font": ("Arial", 10, "bold")}
        ent_style = {"font": ("Arial", 12), "bd": 1, "relief": "solid", "highlightthickness": 0}

        # Username
        tk.Label(card, text="Choose Username", **lbl_style).pack(anchor="w", padx=20)
        self.user_entry = tk.Entry(card, **ent_style)
        self.user_entry.pack(fill="x", padx=20, pady=(5, 20), ipady=8)
        
        # Password
        tk.Label(card, text="Choose Password", **lbl_style).pack(anchor="w", padx=20)
        self.pass_entry = tk.Entry(card, show="*", **ent_style)
        self.pass_entry.pack(fill="x", padx=20, pady=(5, 40), ipady=8)
        
        # Action Button
        tk.Button(card, text="CREATE MY ACCOUNT", bg=colors["accent"], fg="white", 
                  font=("Arial", 12, "bold"), bd=0, cursor="hand2",
                  command=self.handle_signup).pack(fill="x", padx=20, ipady=12)
        
        # Navigation back to Login
        tk.Button(main_container, text="← Already have an account? Sign In", 
                  bg="white", fg="#7f8c8d", bd=0, font=("Arial", 10, "underline"),
                  cursor="hand2", command=lambda: controller.show_frame("LoginWindow")).pack(pady=40)

    def _on_canvas_configure(self, event):
        """Forces the internal frame to match the width of the window."""
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _on_mousewheel(self, event):
        """Allows scrolling with the mouse wheel."""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def handle_signup(self):
        """Handles the registration logic using the brain rules."""
        u, p = self.user_entry.get().strip(), self.pass_entry.get().strip()
        
        if not u or not p:
            messagebox.showwarning("Incomplete", "Please fill in all details!")
            return
            
        # Calling our Brain Rules
        success, msg = add_new_user(u, p)
        if success:
            messagebox.showinfo("Success", msg)
            self.controller.show_frame("LoginWindow")
        else:
            messagebox.showwarning("Warning", msg)