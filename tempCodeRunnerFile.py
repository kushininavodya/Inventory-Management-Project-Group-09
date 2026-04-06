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
        self.title("Kothalawala Mini Mart - POS System")
        self.geometry("700x750")
        self.configure(bg="#f0f2f5")
        self.eval('tk::PlaceWindow . center')
        
        self.colors = {"primary": "#2c3e50", "secondary": "#34495e", "accent": "#27ae60", "bg": "#f0f2f5", "white": "#ffffff", "text": "#333333"}

        self.container = tk.Frame(self, bg="white", bd=1, relief="flat")
        self.container.pack(side="top", fill="both", expand=True, padx=30, pady=30)
        self.container.grid_rowconfigure(0, weight=1); self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginWindow, SignupWindow, MenuWindow, StockWindow, BillingWindow, HistoryWindow):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg="white")

        self.show_frame("LoginWindow")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "on_show"): frame.on_show()
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()