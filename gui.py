import tkinter as tk
from tkinter import messagebox, filedialog
from contact_manager import ContactManager
from whatsapp_automation import WhatsAppAutomation
import config

class ApplicationUI:
    """
    מחלקה האחראית על בניית וניהול הממשק הגרפי (GUI) של המערכת.
    מופרדת לחלוטין מהלוגיקה העסקית.
    """
    def __init__(self, root: tk.Tk):
        self.root = root
        self.contact_manager = ContactManager()
        self.wa_automation = WhatsAppAutomation()
        self.image_path = ""
        
        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        """הגדרות חלון בסיסיות"""
        self.root.title("שולח הודעות אוטומטי - עם בקרה")
        self.root.geometry("450x450")
        self.root.config(bg=config.UI_COLORS["background"])

    def _build_ui(self):
        """בניית כלל רכיבי הממשק"""
        # כותרת
        tk.Label(self.root, text="אוטומציית הודעות לווצאפ", 
                 font=("Helvetica", 18, "bold"), 
                 bg=config.UI_COLORS["background"], 
                 fg=config.UI_COLORS["text"]).pack(pady=15)
        
        # כפתור 1: טעינת תמונה
        tk.Button(self.root, text="1. טען תמונה (JPG/PNG)", 
                  command=self.load_image_handler, 
                  font=("Helvetica", 12), 
                  bg=config.UI_COLORS["button_bg"]).pack(pady=5)
                  
        self.img_status = tk.Label(self.root, text="לא נטענה תמונה", 
                                   font=("Helvetica", 10), 
                                   bg=config.UI_COLORS["background"], 
                                   fg=config.UI_COLORS["text_secondary"])
        self.img_status.pack(pady=2)

        # כפתור 2: טעינת רשימת אנשי קשר
        tk.Button(self.root, text="2. טען קובץ אנשי קשר (CSV)", 
                  command=self.load_csv_handler, 
                  font=("Helvetica", 12), 
                  bg=config.UI_COLORS["button_bg"]).pack(pady=5)
                  
        self.status_label = tk.Label(self.root, text="לא נטען קובץ", 
                                     font=("Helvetica", 10), 
                                     bg=config.UI_COLORS["background"], 
                                     fg=config.UI_COLORS["text_secondary"])
        self.status_label.pack(pady=2)
        
        # תצוגת שם וטלפון של איש הקשר הנוכחי
        self.name_label = tk.Label(self.root, text="", 
                                   font=("Helvetica", 16, "bold"), 
                                   bg=config.UI_COLORS["background"], 
                                   fg=config.UI_COLORS["accent"])
        self.name_label.pack(pady=10)
        
        # כפתור 3: פתיחת הווצאפ
        self.send_btn = tk.Button(self.root, text="3. פתח ווצאפ וצרף הזמנה!", 
                                  command=self.send_message_handler, 
                                  font=("Helvetica", 12, "bold"), 
                                  bg=config.UI_COLORS["success_btn"], 
                                  fg="white", 
                                  activebackground=config.UI_COLORS["success_btn_active"])
        self.send_btn.pack(pady=10, ipadx=10, ipady=5)
        
        # כפתור 4: המעבר לאיש הקשר הבא
        self.next_btn = tk.Button(self.root, text="4. עברתי על ההודעה, הבא ⏭️", 
                                  command=self.next_contact_handler, 
                                  font=("Helvetica", 12), 
                                  bg=config.UI_COLORS["button_bg"])
        self.next_btn.pack(pady=5)

    def load_image_handler(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filepath:
            self.image_path = filepath
            self.img_status.config(text="✅ תמונה נטענה בהצלחה!", fg=config.UI_COLORS["success_text"])

    def load_csv_handler(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return
            
        try:
            self.contact_manager.load_from_csv(filepath)
            self.update_contact_display()
        except Exception as e:
            messagebox.showerror("שגיאה", str(e))

    def update_contact_display(self):
        """מעדכן את התצוגה הגרפית בהתאם לאיש הקשר הנוכחי"""
        if self.contact_manager.has_more_contacts():
            name, phone = self.contact_manager.get_current_contact()
            self.status_label.config(text=self.contact_manager.get_progress_text())
            self.name_label.config(text=f"{name}\n{phone}")
        else:
            self.status_label.config(text="סיימנו את כל הרשימה! 🎉")
            self.name_label.config(text="")

    def send_message_handler(self):
        if not self.image_path:
            messagebox.showwarning("חסר קובץ תמונה", "אנא טען תמונת הזמנה (שלב 1) לפני פתיחת הווצאפ.")
            return
            
        if not self.contact_manager.has_more_contacts():
            messagebox.showwarning("חסרים אנשי קשר", "אנא טען קובץ אנשי קשר (שלב 2) או שהרשימה הסתיימה.")
            return

        try:
            name, phone = self.contact_manager.get_current_contact()
            self.wa_automation.send_invitation(name, phone, self.image_path)
        except Exception as e:
            import traceback
            messagebox.showerror("שגיאה בפתיחת ווצאפ", f"אירעה שגיאה:\n{str(e)}\n\n{traceback.format_exc()}")

    def next_contact_handler(self):
        if not self.contact_manager.has_more_contacts():
            messagebox.showwarning("רשימה ריקה", "אנא טען קובץ אנשי קשר (שלב 2) קודם.")
            return
            
        self.contact_manager.advance_to_next()
        self.update_contact_display()
