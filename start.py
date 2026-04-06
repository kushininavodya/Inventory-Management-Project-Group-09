import tkinter as tk
from screens.login_window import LoginWindow
from screens.signup_window import SignupWindow
from screens.menu_window import MenuWindow
from screens.stock_window import StockWindow
from screens.billing_window import BillingWindow
from screens.history_window import HistoryWindow

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kothalawala Mini Mart - POS")
        
        # Responsive dimensions
        self.geometry("800x800")
        self.minsize(400, 600)
        self.configure(bg="#f0f2f5")
        
        # Global Color Scheme
        self.colors = {
            "primary": "#2c3e50", 
            "secondary": "#34495e", 
            "accent": "#27ae60", 
            "bg": "#f0f2f5", 
            "white": "#ffffff", 
            "text": "#333333"
        }

        # Main Container
        self.container = tk.Frame(self, bg="#f0f2f5")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    
        self.frames = {}
        # We load all your "many windows" here
        for F in (LoginWindow, SignupWindow, MenuWindow, StockWindow, BillingWindow, HistoryWindow):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginWindow")

    def show_frame(self, page_name):
        """Moves the requested window to the front."""
        frame = self.frames[page_name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()