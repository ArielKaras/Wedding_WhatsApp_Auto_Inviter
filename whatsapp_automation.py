import webbrowser
import urllib.parse
import subprocess
import time
import threading
import re
import os

import config
from locales import LOCALES

# ייבוא אוטומטי של pyautogui במידה ואינו מותקן
# Automatic import of pyautogui if not installed
try:
    import pyautogui
except ImportError:
    import os
    os.system('pip install pyautogui')
    import pyautogui

class WhatsAppAutomation:
    """
    מחלקה האחראית על ההתממשקות מול WhatsApp Web:
    פתיחת הדפדפן, עיבוד מספרי הטלפון, והדבקת התמונה.
    
    Class responsible for interacting with WhatsApp Web:
    Opening the browser, processing phone numbers, and pasting the image.
    """
    def __init__(self, lang="he"):
        self.texts = LOCALES.get(lang, LOCALES["he"])
        self.template_file = "message_template.txt"
        self._ensure_template_file()

    def _ensure_template_file(self):
        """
        מוודא שקובץ התבנית קיים. אם לא - יוצר אותו עם טקסט ברירת המחדל.
        Ensures the template file exists. If not, creates it with default text.
        """
        if not os.path.exists(self.template_file):
            with open(self.template_file, "w", encoding="utf-8") as f:
                f.write(self.texts["default_message"])
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """
        מנקה תווים לא חוקיים וממיר מספר מקומי לבינלאומי (ישראל)
        Cleans invalid characters and converts local number to international (Israel)
        """
        clean_phone = re.sub(r'\D', '', phone)
        if clean_phone.startswith('0'):
            clean_phone = '972' + clean_phone[1:]
        return clean_phone

    @staticmethod
    def _auto_paste_clipboard(image_path: str):
        """
        פונקציה פנימית הרצה ברקע:
        מעתיקה את התמונה ללוח העריכה ומדביקה אותה.
        
        Internal background function:
        Copies the image to the clipboard and pastes it.
        """
        # מעתיקים את התמונה ללוח העריכה דרך מנגנון מערכת ההפעלה של Windows
        # Copy the image to the clipboard via Windows OS mechanism
        ps_cmd = f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('{image_path}'))"
        subprocess.run(["powershell", "-command", ps_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
        
        # ממתינים שהדפדפן ו-WhatsApp יטענו לחלוטין
        # Wait for browser and WhatsApp to fully load
        time.sleep(config.WHATSAPP_LOAD_DELAY)
        
        # מדמים לחיצה על Ctrl+V
        # Simulate Ctrl+V press
        pyautogui.hotkey('ctrl', 'v')

    def send_invitation(self, name: str, phone: str, image_path: str):
        """
        מייצר את הקישור לווצאפ, פותח אותו בדפדפן, ומתחיל תהליך רקע להדבקת התמונה.
        
        Generates the WhatsApp link, opens it in the browser, and starts background image pasting.
        """
        clean_phone = self.format_phone(phone)
        
        # קריאת התבנית העדכנית מהקובץ
        # Read the current template from the file
        with open(self.template_file, "r", encoding="utf-8") as f:
            template_text = f.read().strip()
            
        # תכנות מגננתי - בדיקה שהתגית קיימת
        # Defensive programming - ensure {name} tag exists
        if "{name}" not in template_text:
            raise ValueError(self.texts["error_missing_name_tag"])
            
        # מעצבים את ההודעה עם שם איש הקשר
        # Format the message with the contact's name
        message = template_text.format(name=name)
        encoded_message = urllib.parse.quote(message)
        
        # יצירת הלינק ופתיחתו
        # Create and open the link
        url = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"
        webbrowser.open(url)
        
        # מפעילים את פעולת ההדבקה האוטומטית בשרשור נפרד (Thread) כדי לא לתקוע את הממשק
        # Run auto-paste in a separate Thread to avoid freezing the UI
        threading.Thread(target=self._auto_paste_clipboard, args=(image_path,), daemon=True).start()
