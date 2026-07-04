# 🕵️‍♂️ Hiden Text Detector (Pro Edition)

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green)

یک برنامه مبتنی بر پایتون است که برای شناسایی و استخراج داده‌های مخفی از انواع فایل‌ها، از جمله تصاویر، فایل‌های صوتی و آرشیوها طراحی شده است. این برنامه از تکنیک‌های متعددی مانند استگانوگرافی (LSB)، استخراج متادیتای EXIF، OCR، تحلیل متادیتای MP3، محاسبه هش، رمزگشایی Base64، رمزگشایی کلاسیک/XOR و کرک کردن رمز آرشیوها پشتیبانی می‌کند. 
این برنامه دارای رابط کاربری گرافیکی مبتنی بر **Tkinter** با قابلیت کشیدن و رها کردن (Drag & Drop) و سیستم گزارش‌دهی زنده است.

---

## ✨ ویژگی‌ها | Features

- 🖼️ **شناسایی استگانوگرافی:** استخراج داده‌های مخفی در تصاویر با استفاده از استگانوگرافی LSB.
- 📷 **استخراج متادیتای EXIF:** بازیابی متادیتا و اطلاعات پنهان از فایل‌های تصویری.
- 📝 **تحلیل OCR:** شناسایی متن در تصاویر با استفاده از Tesseract OCR (با پشتیبانی از زبان فارسی).
- 🎵 **استخراج متادیتای MP3:** تحلیل متادیتا در فایل‌های صوتی MP3.
- 🔐 **محاسبه هش:** محاسبه هش SHA-256 فایل‌ها.
- 🧩 **رمزگشایی Base64:** استخراج امن رشته‌های متنی از درون فایل‌های باینری و رمزگشایی Base64.
- 🔠 **رمزگشایی کلاسیک/XOR:** بررسی هوشمند و امن انواع فایل‌ها با الگوریتم‌های ROT13، سزار و XOR روی بایت‌ها.
- 💣 **کرک آرشیو (Memory-Safe):** کرک رمز فایل‌های ZIP و RAR با وردلیست‌های فوق حجیم بدون مصرف RAM اضافی (طراحی Lazy Loading).
- 🔍 **تحلیل Hex EOF:** جستجوی بایت‌های جادویی (Magic Bytes) برای یافتن فایل‌های مخفی در انتهای سایر فایل‌ها.
- 🖥️ **رابط کاربری حرفه‌ای:** رابط کاربری Tkinter کاملاً Thread-Safe دارای نوار پیشرفت (Progress Bar) و گزارش‌دهی زنده.

---

## 📁 انواع فایل‌های پشتیبانی‌شده | Supported Files

- 🖼️ **تصاویر:** `.jpg`, `.png`, `.jpeg`
- 🎧 **صوت:** `.mp3`
- 🗄️ **آرشیوها:** `.zip`, `.rar`
- 📄 **متن:** `.txt`

---

## ⚙️ پیش‌نیازها | Prerequisites

- 💻 **سیستم‌عامل:** ویندوز، لینوکس یا macOS
- 🐍 **پایتون:** نسخه ۳.۸ یا بالاتر

### 📦 وابستگی‌های پایتون
برای نصب پکیج‌های مورد نیاز، فایل `requirements.txt` در دسترس است:
```bash
pip install -r requirements.txt
```
*(شامل پکیج‌های: pillow, pytesseract, stegano, exifread, python-magic, mutagen, tkinterdnd2, rarfile)*

### 🛠️ نیازهای سیستمی اضافی (System Requirements)

🔹 **Tesseract OCR:** برای استخراج متن از عکس ضروری است.
- **در اوبونتو:** `sudo apt install tesseract-ocr tesseract-ocr-fas`
- **در ویندوز:** دانلود و نصب از مخزن گیت‌هاب Tesseract و افزودن به مسیر PATH سیستم.

🔹 **libmagic:** برای شناسایی دقیق نوع فایل‌ها.
- **در اوبونتو:** `sudo apt install libmagic1`
- **در ویندوز:** `pip install python-magic-bin`

🔹 **unrar:** برای باز کردن و استخراج فایل‌های RAR مخفی.
- **در اوبونتو:** `sudo apt install unrar`
- **در ویندوز:** دانلود `unrar.dll` و اطمینان از دسترسی سیستمی به آن.

---

## 🚀 استفاده | Usage

۱. **اجرای اسکریپت:**
   ```bash
   python3 Hiden-Text-Detector.py
   ```
۲. **در رابط کاربری (GUI):**
   - 📂 یک پوشه را بکشید و رها کنید (Drag & Drop) یا روی "Select Folder" کلیک کنید.
   - 📖 *(اختیاری)* روی "Select Wordlist" کلیک کنید تا یک فایل وردلیست برای شکستن قفل آرشیوها بارگذاری شود.
   - ▶️ روی "**Start Scan**" کلیک کنید تا اسکن آغاز شود.
   - 📊 نتایج را در پنجره لاگ پایین صفحه ببینید. داده‌های مخفی با رنگ **سبز** و خطاها با رنگ **قرمز** مشخص می‌شوند.
   - 🛑 برای توقف فرآیند در هر زمان، روی "**Stop Scan**" کلیک کنید.

> 📝 **توجه:** لاگ‌های داده‌های مخفی به‌صورت خودکار در فایلی به نام `scan_log.txt` در همان پوشه ذخیره می‌شوند.

---

## 💡 نکات | Notes

- ⏳ **عملکرد:** اسکن پوشه‌های حجیم یا کرک فایل‌های فشرده با وردلیست‌های چند گیگابایتی زمان‌بر است، اما به لطف طراحی جدید، رابط کاربری قفل نخواهد کرد.
- 🔑 **وردلیست:** برای پیدا کردن پسورد فایل‌های ZIP و RAR حتماً باید یک فایل وردلیست معتبر آپلود کنید.
- 🇮🇷 **زبان OCR:** سیستم OCR روی زبان فارسی (`fas`) تنظیم شده است. برای زبان‌های دیگر می‌توانید در سورس‌کد پارامتر زبان را تغییر دهید (`fas+eng`).

---

---

# 🇬🇧 English Documentation

## 🕵️‍♂️ Hiden Text Detector

The **Hidden Text Detector** is a powerful Python-based application designed to detect and extract hidden data from various file types, including images, audio files, and archives. It features a thread-safe **Tkinter GUI** with drag-and-drop functionality and real-time logs.

## ✨ Features

- 🖼️ **Steganography Detection:** Extracts hidden data in images using LSB steganography.
- 📷 **EXIF Metadata:** Retrieves hidden metadata from image files.
- 📝 **OCR Analysis:** Detects text in images using Tesseract OCR.
- 🎵 **MP3 Metadata:** Analyzes and extracts metadata from MP3 files.
- 🔐 **Hash Calculation:** Computes SHA-256 hashes of analyzed files.
- 🧩 **Base64 Decoding:** Safely extracts printable strings from binary files to decode Base64 data.
- 🔠 **Classic/XOR Decryption:** Robust byte-level XOR and ROT13/Caesar analysis for all supported files.
- 💣 **Archive Brute-Forcing:** Memory-safe (lazy-loaded) brute-forcing for ZIP and RAR passwords.
- 🔍 **Hex EOF Analysis:** Detects hidden ZIP or RAR files appended to the end of other files via magic bytes.
- 🖥️ **Thread-Safe GUI:** Progress bar and real-time scan logs without UI freezing.

## 📁 Supported File Types
- Images: `.jpg`, `.png`, `.jpeg`
- Audio: `.mp3`
- Archives: `.zip`, `.rar`
- Text: `.txt`

## ⚙️ Prerequisites

**System:** Windows, Linux, or macOS  
**Python:** 3.8+

Install Python dependencies:
```bash
pip install -r requirements.txt
```

**System Dependencies:**
- **Tesseract OCR:** Required for reading text from images. (`sudo apt install tesseract-ocr tesseract-ocr-fas`)
- **libmagic:** Required for accurate file type detection. (`sudo apt install libmagic1`)
- **unrar:** Required for extracting RAR files. (`sudo apt install unrar`)

## 🚀 Usage

Run the detector:
```bash
python3 Hiden-Text-Detector.py
```

Then simply select or drag-and-drop a folder to analyze, attach a Wordlist if you want to crack archives, and press **Start Scan**!

---

## 📄 License | لایسنس

This project is licensed under the [MIT License](LICENSE).  
این پروژه تحت لایسنس MIT منتشر شده است.

![Repo Badge](https://visitor-badge.laobi.icu/badge?page_id=null-err0r.Hiden-Text-Detector) 
