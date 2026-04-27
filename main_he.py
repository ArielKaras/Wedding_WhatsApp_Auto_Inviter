import tkinter as tk
from gui import ApplicationUI

"""
נקודת הכניסה לגרסה העברית (Hebrew Entry Point).
"""

def main():
    root = tk.Tk()
    app = ApplicationUI(root, lang='he')
    root.mainloop()

if __name__ == "__main__":
    main()
