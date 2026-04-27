import csv

class ContactManager:
    """
    מחלקה האחראית על ניהול מידע אנשי הקשר: 
    קריאה מקובץ, ולידציה, ומעקב אחר המיקום הנוכחי ברשימה.
    """
    def __init__(self):
        self.contacts = []
        self.current_index = 0

    def load_from_csv(self, filepath: str) -> int:
        """
        טוען אנשי קשר מקובץ CSV.
        מחזיר את מספר אנשי הקשר שנטענו בהצלחה.
        """
        new_contacts = []
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    phone = row[1].strip()
                    # מוודאים שיש שם ושיש ספרות בטלפון
                    if name and phone and any(c.isdigit() for c in phone):
                        new_contacts.append((name, phone))
        
        if not new_contacts:
            raise ValueError("לא נמצאו אנשי קשר תקינים בקובץ.\nוודאו שהקובץ בפורמט CSV ושעמודות א' וב' מלאות.")
        
        self.contacts = new_contacts
        self.current_index = 0
        return len(self.contacts)

    def get_current_contact(self):
        """מחזיר את איש הקשר הנוכחי (שם, טלפון) או None אם סיימנו"""
        if self.has_more_contacts():
            return self.contacts[self.current_index]
        return None

    def advance_to_next(self):
        """מקדם את האינדקס לאיש הקשר הבא"""
        self.current_index += 1

    def has_more_contacts(self) -> bool:
        """בודק אם נשארו עוד אנשי קשר ברשימה"""
        return 0 <= self.current_index < len(self.contacts)
    
    def get_progress_text(self) -> str:
        """מחזיר טקסט המציג את ההתקדמות (למשל: איש קשר 1 מתוך 10)"""
        if self.contacts:
            return f"איש קשר {self.current_index + 1} מתוך {len(self.contacts)}"
        return "לא נטען קובץ"
