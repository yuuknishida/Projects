from Window import Window

class ToDoListApp:
    def __init__(self):
        self.window = Window()

    def run(self):
        self.window.window.mainloop()

if __name__ == "__main__":  # pragma: no cover
    app = ToDoListApp()
    app.run()