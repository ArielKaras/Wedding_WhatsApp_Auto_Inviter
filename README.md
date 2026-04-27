# WhatsApp Auto Inviter ✉️💖

A simple, user-friendly automation tool for sending personalized WhatsApp messages directly from a contacts list (CSV).
This tool is built around the **Human-in-the-Loop** philosophy — the automation prepares the message and image for you, but the final decision and clicking the "Send" button on WhatsApp remains in your hands. This prevents "human errors" and embarrassing mistakes when sending mass invitations.

## Features
* 📂 **List Parsing**: Load names and phone numbers from an Excel (CSV) file.
* 📝 **Personalization**: Generate a generic text message that automatically integrates the recipient's name.
* 🖼️ **Image Attachment**: Automatically copies and pastes your invitation image directly into the chat window.
* 🛡️ **Human Oversight**: You control the pace of moving between contacts to ensure no one is missed.

## Prerequisites
To use this system, ensure you have [Python](https://www.python.org/downloads/) installed.
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

## How to Run
1. Download all project files to your computer.
2. Open the command line (Terminal / CMD) in the project directory.
3. Run the following command:
   ```bash
   python main.py
   ```
4. In the application window:
   * **Step 1**: Click `Load Image` and select your invitation image.
   * **Step 2**: Click `Load Contacts (CSV)` and select your prepared CSV file.
   * **Step 3**: Click `Open WhatsApp & Attach!`. The system will open the browser, load the text, and paste the image (make sure not to touch the mouse/keyboard during the pasting process).
   * **Step 4**: Send the message on WhatsApp, then return to the application and click `Next` for the next contact.

## Customizing the Message Text
You can easily modify the generic message content and design by editing the `config.py` file.
Locate the `DEFAULT_MESSAGE` variable and change the text as desired (make sure to leave the `{name}` placeholder where you want the contact's name to appear).

---
*This project was created as a solution to human errors and the desire to streamline everyday technical processes without losing the personal touch.*
