from Window import *

def main():
    app = QApplication(sys.argv)
    window = AppMainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()