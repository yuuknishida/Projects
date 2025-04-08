import tkinter as tk
class Window(tk.Tk):
    """Represents the window of the application"""
    def __init__(self):
        self.width = 800
        self.height = 800

        self.window = tk.Tk()
        self.window.title("ToDoList App")

        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack()

        # Create the main content area
        self.content_frame = tk.Frame(self.window)
        self.content_frame.pack(side="left", fill="both", expand=True)
        
    def create_buttons(self):
        """Creates the buttons for the sidebar
        -   Settings
        -   TaskHistory
        -   TaskForm
        """
        self.settings = tk.Button(self.canvas, text="Settings", command=self.button_clicked)
        self.settings.pack(pady=10)

    def button_clicked(self):
        print("Button clicked")
        self.clear_content()

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()