# WhatsApp Auto Inviter ✉️💖

A simple, user-friendly automation tool for sending personalized WhatsApp messages directly from a contacts list (CSV).
This tool is built around the **Human-in-the-Loop** philosophy — the automation prepares the message and image for you, but the final decision and clicking the "Send" button on WhatsApp remains in your hands. This prevents "human errors" and embarrassing mistakes when sending mass invitations.

## Features
* 📂 **List Parsing**: Load names and phone numbers from an Excel (CSV) file.
* 📝 **Personalization**: Generate a generic text message that automatically integrates the recipient's name.
* 🖼️ **Image Attachment**: Automatically copies and pastes your invitation image directly into the chat window.
* 🛡️ **Human Oversight**: You control the pace of moving between contacts to ensure no one is missed.

## 🚀 How to Download & Run (No Code Required)
You can simply download the ready-to-use executable without installing Python!

1. Go to the **Releases** tab on the right side of this GitHub repository.
2. Download the version you prefer:
   * `WhatsApp_Auto_Inviter_EN.exe` (English Interface)
   * `WhatsApp_Auto_Inviter_HE.exe` (Hebrew Interface)
3. Double-click the `.exe` file to start the application.

> [!WARNING]
> **Windows Defender (SmartScreen) False Positive**
> Because this is a custom-built `.exe` file using `PyInstaller` (and not digitally signed by a paid certificate), Windows Defender might show a blue warning screen saying "Windows protected your PC".
> **This is completely normal for open-source tools.**
> To run the app, simply click **"More info"** on the blue screen, and then click the **"Run anyway"** button.

## Prerequisites (If running from source)
To run the source code directly, ensure you have [Python](https://www.python.org/downloads/) installed.
The core automation library will be installed automatically upon first run:
* `pyautogui` (auto-installed if missing).

## Preparation: Required Files
Before running the application, you **must prepare two files**:

1. **Invitation Image**: An image in JPG or PNG format.
2. **Contacts File (CSV)**: 
   To create this, open a new Excel file and arrange it as follows:
   * **Column A**: Recipient names (e.g., John Doe).
   * **Column B**: Phone numbers (e.g., 0501234567).
   * *Note: Column headers are not required; the software reads the rows directly.*
   * Save the file: `File` -> `Save As` -> Choose the format `CSV UTF-8 (Comma delimited) (*.csv)`.

## How to Run from Source
1. Download all project files to your computer.
2. Open the command line (Terminal / CMD) in the project directory.
3. Run one of the following commands based on your language preference:
   ```bash
   python main_en.py  # For English
   # OR
   python main_he.py  # For Hebrew
   ```
4. In the application window:
   * **Step 1**: Click `Load Image` and select your invitation image.
   * **Step 2**: Click `Load Contacts (CSV)` and select your prepared CSV file.
   * **Step 3**: Click `Open WhatsApp & Attach!`. The system will open the browser, load the text, and paste the image (make sure not to touch the mouse/keyboard during the pasting process).
   * **Step 4**: Send the message on WhatsApp, then return to the application and click `Next` for the next contact.

## Customizing the Message Text
You do not need to modify any code to customize your invitation message!
When you run the application for the first time, it will automatically create a file named `message_template.txt` in the same folder.
* Open `message_template.txt` in any text editor (like Notepad).
* Edit the message to whatever you like.
* **Important:** Make sure to leave the `{name}` placeholder where you want the recipient's name to appear!
* Save the file, and the application will automatically use your new text for all messages.

---
*This project was created as a solution to human errors and the desire to streamline everyday technical processes without losing the personal touch.*
