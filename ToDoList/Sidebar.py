import tkinter as tk
from PIL import Image, ImageTk
class Sidebar(tk.Tk):
    """Sidebar for the application"""
    def __init__(self):
        super().__init__()
        self.geometry("200x800")
        self.title("Sidebar")
        self.resizable(False, False)

        self.frame = tk.Frame(self, width=200, bg="gray")
        self.frame.pack(side="left", fill="y")

        # buttons for the sidebar
    
    def createButtons(self, name):
        self.buttons = []
        pass