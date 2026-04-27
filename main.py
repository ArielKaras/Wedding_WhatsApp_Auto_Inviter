import tkinter as tk
from gui import ApplicationUI

"""
נקודת הכניסה הראשית של המערכת (Entry Point).
כאן נוצר החלון הראשי והאפליקציה מתחילה לרוץ.
"""

def main():
    root = tk.Tk()
    app = ApplicationUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
