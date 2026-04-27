import webbrowser
import urllib.parse
import subprocess
import time
import threading
import re

import config

# ייבוא אוטומטי של pyautogui במידה ואינו מותקן
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
    """
    
    @staticmethod
    def format_phone(phone: str) -> str:
        """מנקה תווים לא חוקיים וממיר מספר מקומי לבינלאומי (ישראל)"""
        clean_phone = re.sub(r'\D', '', phone)
        if clean_phone.startswith('0'):
            clean_phone = '972' + clean_phone[1:]
        return clean_phone

    @staticmethod
    def _auto_paste_clipboard(image_path: str):
        """
        פונקציה פנימית הרצה ברקע:
        מעתיקה את התמונה ללוח העריכה ומדביקה אותה.
        """
        # מעתיקים את התמונה ללוח העריכה דרך מנגנון מערכת ההפעלה של Windows
        ps_cmd = f"Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.Clipboard]::SetImage([System.Drawing.Image]::FromFile('{image_path}'))"
        subprocess.run(["powershell", "-command", ps_cmd], creationflags=subprocess.CREATE_NO_WINDOW)
        
        # ממתינים שהדפדפן ו-WhatsApp יטענו לחלוטין
        time.sleep(config.WHATSAPP_LOAD_DELAY)
        
        # מדמים לחיצה על Ctrl+V
        pyautogui.hotkey('ctrl', 'v')

    def send_invitation(self, name: str, phone: str, image_path: str):
        """
        מייצר את הקישור לווצאפ, פותח אותו בדפדפן, ומתחיל תהליך רקע להדבקת התמונה.
        """
        clean_phone = self.format_phone(phone)
        
        # מעצבים את ההודעה עם שם איש הקשר
        message = config.DEFAULT_MESSAGE.format(name=name)
        encoded_message = urllib.parse.quote(message)
        
        # יצירת הלינק ופתיחתו
        url = f"https://api.whatsapp.com/send?phone={clean_phone}&text={encoded_message}"
        webbrowser.open(url)
        
        # מפעילים את פעולת ההדבקה האוטומטית בשרשור נפרד (Thread) כדי לא לתקוע את הממשק
        threading.Thread(target=self._auto_paste_clipboard, args=(image_path,), daemon=True).start()
