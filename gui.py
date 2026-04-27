import tkinter as tk
from tkinter import messagebox, filedialog
from contact_manager import ContactManager
from whatsapp_automation import WhatsAppAutomation
import config
from locales import LOCALES

class ApplicationUI:
    """
    מחלקה האחראית על בניית וניהול הממשק הגרפי (GUI) של המערכת.
    מופרדת לחלוטין מהלוגיקה העסקית.
    
    Class responsible for building and managing the Graphical User Interface (GUI).
    Completely separated from the business logic.
    """
    def __init__(self, root: tk.Tk, lang: str = "he"):
        self.root = root
        self.lang = lang
        self.texts = LOCALES.get(lang, LOCALES["he"])
        self.contact_manager = ContactManager(lang=lang)
        self.wa_automation = WhatsAppAutomation(lang=lang)
        self.image_path = ""
        
        self._setup_window()
        self._build_ui()

    def _setup_window(self):
        """
        הגדרות חלון בסיסיות
        Basic window configurations
        """
        self.root.title(self.texts["window_title"])
        self.root.geometry("450x450")
        self.root.config(bg=config.UI_COLORS["background"])

    def _build_ui(self):
        """
        בניית כלל רכיבי הממשק
        Building all UI components
        """
        # Determine alignment
        align = "right" if self.texts["rtl"] else "left"
        anchor = "e" if self.texts["rtl"] else "w"

        # כותרת
        # Title
        tk.Label(self.root, text=self.texts["main_title"], 
                 font=("Helvetica", 18, "bold"), 
                 bg=config.UI_COLORS["background"], 
                 fg=config.UI_COLORS["text"],
                 justify=align).pack(pady=15)
        
        # כפתור 1: טעינת תמונה
        # Button 1: Load Image
        tk.Button(self.root, text=self.texts["btn_load_image"], 
                  command=self.load_image_handler, 
                  font=("Helvetica", 12), 
                  bg=config.UI_COLORS["button_bg"]).pack(pady=5)
                  
        self.img_status = tk.Label(self.root, text=self.texts["status_no_image"], 
                                   font=("Helvetica", 10), 
                                   bg=config.UI_COLORS["background"], 
                                   fg=config.UI_COLORS["text_secondary"],
                                   justify=align)
        self.img_status.pack(pady=2)

        # כפתור 2: טעינת רשימת אנשי קשר
        # Button 2: Load Contacts List
        tk.Button(self.root, text=self.texts["btn_load_csv"], 
                  command=self.load_csv_handler, 
                  font=("Helvetica", 12), 
                  bg=config.UI_COLORS["button_bg"]).pack(pady=5)
                  
        self.status_label = tk.Label(self.root, text=self.texts["status_no_csv"], 
                                     font=("Helvetica", 10), 
                                     bg=config.UI_COLORS["background"], 
                                     fg=config.UI_COLORS["text_secondary"],
                                     justify=align)
        self.status_label.pack(pady=2)
        
        # תצוגת שם וטלפון של איש הקשר הנוכחי
        # Display name and phone of current contact
        self.name_label = tk.Label(self.root, text="", 
                                   font=("Helvetica", 16, "bold"), 
                                   bg=config.UI_COLORS["background"], 
                                   fg=config.UI_COLORS["accent"],
                                   justify=align)
        self.name_label.pack(pady=10)
        
        # כפתור 3: פתיחת הווצאפ
        # Button 3: Open WhatsApp
        self.send_btn = tk.Button(self.root, text=self.texts["btn_open_whatsapp"], 
                                  command=self.send_message_handler, 
                                  font=("Helvetica", 12, "bold"), 
                                  bg=config.UI_COLORS["success_btn"], 
                                  fg="white", 
                                  activebackground=config.UI_COLORS["success_btn_active"])
        self.send_btn.pack(pady=10, ipadx=10, ipady=5)
        
        # כפתור 4: המעבר לאיש הקשר הבא
        # Button 4: Move to next contact
        self.next_btn = tk.Button(self.root, text=self.texts["btn_next_contact"], 
                                  command=self.next_contact_handler, 
                                  font=("Helvetica", 12), 
                                  bg=config.UI_COLORS["button_bg"])
        self.next_btn.pack(pady=5)

    def load_image_handler(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filepath:
            self.image_path = filepath
            self.img_status.config(text=self.texts["status_image_loaded"], fg=config.UI_COLORS["success_text"])

    def load_csv_handler(self):
        filepath = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not filepath:
            return
            
        try:
            self.contact_manager.load_from_csv(filepath)
            self.update_contact_display()
        except Exception as e:
            messagebox.showerror(self.texts["error_title"], str(e))

    def update_contact_display(self):
        """
        מעדכן את התצוגה הגרפית בהתאם לאיש הקשר הנוכחי
        Updates the graphical display according to the current contact
        """
        if self.contact_manager.has_more_contacts():
            name, phone = self.contact_manager.get_current_contact()
            self.status_label.config(text=self.contact_manager.get_progress_text())
            self.name_label.config(text=f"{name}\n{phone}")
        else:
            self.status_label.config(text=self.texts["status_finished"])
            self.name_label.config(text="")

    def send_message_handler(self):
        if not self.image_path:
            messagebox.showwarning(self.texts["warning_no_image_title"], self.texts["warning_no_image_text"])
            return
            
        if not self.contact_manager.has_more_contacts():
            messagebox.showwarning(self.texts["warning_no_csv_title"], self.texts["warning_no_csv_text"])
            return

        try:
            name, phone = self.contact_manager.get_current_contact()
            self.wa_automation.send_invitation(name, phone, self.image_path)
        except Exception as e:
            import traceback
            err_msg = self.texts["whatsapp_error_text"].format(error=str(e), traceback=traceback.format_exc())
            messagebox.showerror(self.texts["whatsapp_error_title"], err_msg)

    def next_contact_handler(self):
        if not self.contact_manager.has_more_contacts():
            messagebox.showwarning(self.texts["warning_empty_list_title"], self.texts["warning_empty_list_text"])
            return
            
        self.contact_manager.advance_to_next()
        self.update_contact_display()
