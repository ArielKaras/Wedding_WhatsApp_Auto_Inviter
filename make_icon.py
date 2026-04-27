from PIL import Image, ImageDraw, ImageFont

def create_icon():
    # יצירת תמונה בסיסית בצבע ירוק (כמו ווצאפ)
    img = Image.new('RGBA', (256, 256), color=(37, 211, 102, 255))
    d = ImageDraw.Draw(img)
    
    # ציור מסגרת פנימית קטנה (עיגול לבן)
    d.ellipse([(20, 20), (236, 236)], outline=(255, 255, 255, 255), width=10)
    
    # נוסיף את האות "W" באמצע, או סתם מעטפה
    # נצייר צורה פשוטה של מעטפה פתוחה / מכתב
    # מלבן למעטפה
    d.rectangle([(60, 90), (196, 170)], outline=(255, 255, 255, 255), width=8)
    # קווי הקיפול של המעטפה
    d.line([(60, 90), (128, 140)], fill=(255, 255, 255, 255), width=8)
    d.line([(128, 140), (196, 90)], fill=(255, 255, 255, 255), width=8)
    
    # שמירה בפורמט ICO
    img.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])

if __name__ == "__main__":
    create_icon()
