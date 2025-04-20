# Hiden Text Detector


The Hidden Text Detector is a Python-based application designed to detect and extract hidden data from various file types, including images, audio files, and archives. It supports multiple techniques such as steganography (LSB), EXIF metadata extraction, OCR, MP3 metadata analysis, hash calculation, Base64 decoding, classic/XOR decryption, and brute-forcing archive passwords. The application features a user-friendly Tkinter GUI with drag-and-drop support and a log system to track findings.
Features

Steganography Detection: Extracts hidden data in images using LSB (Least Significant Bit) steganography.
EXIF Metadata Extraction: Retrieves metadata from image files.
OCR Analysis: Detects text in images using Tesseract OCR (with Persian language support).
MP3 Metadata Extraction: Analyzes metadata in MP3 audio files.
Hash Calculation: Computes SHA-256 hash of files.
Base64 Decoding: Attempts to decode file content as Base64.
Classic/XOR Decryption: Applies ROT13, Caesar cipher, and XOR decryption to text content.
Archive Brute-Forcing: Attempts to crack ZIP and RAR archive passwords using a wordlist.
Hex EOF Analysis: Detects hidden ZIP or RAR files appended to file ends.
GUI: Tkinter-based interface with drag-and-drop folder selection and real-time scan logs.

Supported File Types

Images: .jpg, .png, .jpeg
Audio: .mp3
Archives: .zip, .rar

Prerequisites

Operating System: Windows, Linux, or macOS
Python: Version 3.8 or higher
Dependencies:
Install required Python packages:
pip install pillow pytesseract stegano exifread python-magic mutagen tkinterdnd2


Additional system requirements:

Tesseract OCR: Install Tesseract and ensure it's in your system PATH.
On Ubuntu: sudo apt install tesseract-ocr tesseract-ocr-fas
On Windows: Download and install from Tesseract GitHub


libmagic: Required for file type detection.
On Ubuntu: sudo apt install libmagic1
On Windows: Install python-magic-bin (pip install python-magic-bin)


unrar: For RAR file support.
On Ubuntu: sudo apt install unrar
On Windows: Install unrar.dll and ensure it's accessible.






Optional:
A wordlist file (.txt) for brute-forcing archive passwords.



Install dependencies:
pip install -r requirements.txt



Install system dependencies:


sudo apt install tesseract-ocr tesseract-ocr-fas libmagic1 unrar


For Windows:

Install Tesseract OCR and add it to your PATH.
Install python-magic-bin for file type detection.
Ensure unrar.dll is installed for RAR support.




(Optional) Prepare a wordlist file for archive brute-forcing.


Usage

Run the script:
python3 Hiden-Text-Detector.py


In the GUI:

Drag and drop a folder or click "Select Folder" to choose a directory.
(Optional) Click "Select Wordlist" to load a wordlist for archive password cracking.
Click "Start Scan" to begin analyzing files.
View results in the scrollable text area. Hidden data is highlighted in green, errors in red.
Click "Stop Scan" to halt the process.


Logs of hidden data are saved to scan_log.txt in the project directory.


Notes

Performance: Scanning large folders or brute-forcing archives with large wordlists can be time-consuming.
Wordlist: Brute-forcing requires a wordlist file. Without it, archive password cracking is skipped.
Language Support: OCR is configured for Persian (fas). Modify the lang parameter in extract_ocr for other languages.
File Types: Only supported file types (.jpg, .png, .jpeg, .mp3, .zip, .rar) are analyzed.
Log File: Ensure write permissions for scan_log.txt in the project directory.




 یک برنامه مبتنی بر پایتون است که برای شناسایی و استخراج داده‌های مخفی از انواع فایل‌ها، از جمله تصاویر، فایل‌های صوتی و آرشیوها طراحی شده است. این برنامه از تکنیک‌های متعددی مانند استگانوگرافی (LSB)، استخراج متادیتای EXIF، OCR، تحلیل متادیتای MP3، محاسبه هش، رمزگشایی Base64، رمزگشایی کلاسیک/XOR و کرک کردن رمز آرشیوها پشتیبانی می‌کند. این برنامه دارای رابط کاربری گرافیکی مبتنی بر Tkinter با قابلیت کشیدن و رها کردن و سیستم لاگ برای ردیابی یافته‌ها است.
ویژگی‌ها

شناسایی استگانوگرافی: استخراج داده‌های مخفی در تصاویر با استفاده از استگانوگرافی LSB.
استخراج متادیتای EXIF: بازیابی متادیتا از فایل‌های تصویری.
تحلیل OCR: شناسایی متن در تصاویر با استفاده از Tesseract OCR (با پشتیبانی از زبان فارسی).
استخراج متادیتای MP3: تحلیل متادیتا در فایل‌های صوتی MP3.
محاسبه هش: محاسبه هش SHA-256 فایل‌ها.
رمزگشایی Base64: تلاش برای رمزگشایی محتوای فایل به‌صورت Base64.
رمزگشایی کلاسیک/XOR: اعمال رمزگشایی ROT13، رمز سزار و XOR به محتوای متنی.
کرک آرشیو: تلاش برای کرک رمز فایل‌های ZIP و RAR با استفاده از وردلیست.
تحلیل Hex EOF: شناسایی فایل‌های ZIP یا RAR مخفی در انتهای فایل‌ها.
رابط کاربری: رابط مبتنی بر Tkinter با قابلیت انتخاب پوشه با کشیدن و رها کردن و لاگ‌های اسکن در زمان واقعی.

انواع فایل‌های پشتیبانی‌شده

تصاویر: .jpg, .png, .jpeg
صوت: .mp3
آرشیوها: .zip, .rar

پیش‌نیازها

سیستم‌عامل: ویندوز، لینوکس یا macOS
پایتون: نسخه ۳.۸ یا بالاتر
وابستگی‌ها:
نصب پکیج‌های پایتون مورد نیاز:
pip install pillow pytesseract stegano exifread python-magic mutagen tkinterdnd2


نیازهای سیستمی اضافی:

Tesseract OCR: نصب Tesseract و اطمینان از وجود آن در PATH سیستم.
در اوبونتو: sudo apt install tesseract-ocr tesseract-ocr-fas
در ویندوز: دانلود و نصب از Tesseract GitHub


libmagic: برای شناسایی نوع فایل مورد نیاز است.
در اوبونتو: sudo apt install libmagic1
در ویندوز: نصب python-magic-bin (pip install python-magic-bin)


unrar: برای پشتیبانی از فایل‌های RAR.
در اوبونتو: sudo apt install unrar
در ویندوز: نصب unrar.dll و اطمینان از دسترسی به آن.






اختیاری:
یک فایل وردلیست (.txt) برای کرک رمز آرشیوها.




وابستگی‌ها را نصب کنید:
pip install -r requirements.txt

یک فایل requirements.txt با محتوای زیر ایجاد کنید:

نصب وابستگی‌های سیستمی:

برای اوبونتو:
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-fas libmagic1 unrar


برای ویندوز:

نصب Tesseract OCR و افزودن آن به PATH.
نصب python-magic-bin برای شناسایی نوع فایل.
اطمینان از نصب unrar.dll برای پشتیبانی از RAR.




(اختیاری) یک فایل وردلیست برای کرک رمز آرشیوها آماده کنید.


استفاده

اسکریپت را اجرا کنید:
python3 Hiden-Text-Detector.py


در رابط کاربری:

یک پوشه را با کشیدن و رها کردن یا کلیک روی "Select Folder" انتخاب کنید.
(اختیاری) روی "Select Wordlist" کلیک کنید تا یک وردلیست برای کرک رمز آرشیوها بارگذاری شود.
روی "Start Scan" کلیک کنید تا اسکن فایل‌ها آغاز شود.
نتایج را در ناحیه متنی قابل پیمایش مشاهده کنید. داده‌های مخفی به رنگ سبز و خطاها به رنگ قرمز نمایش داده می‌شوند.
برای توقف فرآیند روی "Stop Scan" کلیک کنید.


لاگ‌های داده‌های مخفی در scan_log.txt در پوشه پروژه ذخیره می‌شوند.


نکات

عملکرد: اسکن پوشه‌های بزرگ یا کرک آرشیوها با وردلیست‌های بزرگ ممکن است زمان‌بر باشد.
وردلیست: کرک رمز آرشیوها به یک فایل وردلیست نیاز دارد. بدون آن، کرک رمز انجام نمی‌شود.
پشتیبانی از زبان: OCR برای زبان فارسی (fas) تنظیم شده است. برای زبان‌های دیگر، پارامتر lang در تابع extract_ocr را تغییر دهید.
انواع فایل: فقط فایل‌های پشتیبانی‌شده (.jpg, .png, .jpeg, .mp3, .zip, .rar) تحلیل می‌شوند.
فایل لاگ: اطمینان حاصل کنید که برای scan_log.txt در پوشه پروژه مجوز نوشتن وجود دارد.


