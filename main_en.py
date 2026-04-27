import tkinter as tk
from gui import ApplicationUI

"""
English Entry Point.
"""

def main():
    root = tk.Tk()
    app = ApplicationUI(root, lang='en')
    root.mainloop()

if __name__ == "__main__":
    main()
