import csv
from locales import LOCALES

class ContactManager:
    """
    מחלקה האחראית על ניהול מידע אנשי הקשר: 
    קריאה מקובץ, ולידציה, ומעקב אחר המיקום הנוכחי ברשימה.
    
    Class responsible for managing contact information:
    Reading from a file, validation, and tracking the current position in the list.
    """
    def __init__(self, lang="he"):
        self.contacts = []
        self.current_index = 0
        self.texts = LOCALES.get(lang, LOCALES["he"])

    def load_from_csv(self, filepath: str) -> int:
        """
        טוען אנשי קשר מקובץ CSV.
        מחזיר את מספר אנשי הקשר שנטענו בהצלחה.
        
        Loads contacts from a CSV file.
        Returns the number of contacts successfully loaded.
        """
        new_contacts = []
        with open(filepath, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    name = row[0].strip()
                    phone = row[1].strip()
                    # מוודאים שיש שם ושיש ספרות בטלפון
                    # Ensure there is a name and digits in the phone number
                    if name and phone and any(c.isdigit() for c in phone):
                        new_contacts.append((name, phone))
        
        if not new_contacts:
            raise ValueError(self.texts["error_no_contacts"])
        
        self.contacts = new_contacts
        self.current_index = 0
        return len(self.contacts)

    def get_current_contact(self):
        """
        מחזיר את איש הקשר הנוכחי (שם, טלפון) או None אם סיימנו
        Returns the current contact (name, phone) or None if finished
        """
        if self.has_more_contacts():
            return self.contacts[self.current_index]
        return None

    def advance_to_next(self):
        """
        מקדם את האינדקס לאיש הקשר הבא
        Advances the index to the next contact
        """
        self.current_index += 1

    def has_more_contacts(self) -> bool:
        """
        בודק אם נשארו עוד אנשי קשר ברשימה
        Checks if there are more contacts in the list
        """
        return 0 <= self.current_index < len(self.contacts)
    
    def get_progress_text(self) -> str:
        """
        מחזיר טקסט המציג את ההתקדמות (למשל: איש קשר 1 מתוך 10)
        Returns text showing progress (e.g., Contact 1 of 10)
        """
        if self.contacts:
            return self.texts["status_progress"].format(current=self.current_index + 1, total=len(self.contacts))
        return self.texts["status_no_csv"]
