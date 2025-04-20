#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image
import pytesseract
from stegano import lsb
import exifread
import base64
import hashlib
import binascii
import magic
import threading
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import zipfile
import rarfile

class SteganoExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hiden Text Detector - Demo Edition")
        self.root.geometry("800x600")
        self.stop_flag = False

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.folder_entry = tk.Entry(self.frame, width=50)
        self.folder_entry.pack(side=tk.LEFT, padx=10)
        self.folder_entry.drop_target_register(DND_FILES)
        self.folder_entry.dnd_bind('<<Drop>>', self.drop)

        self.browse_button = tk.Button(self.frame, text="Select Folder", command=self.browse_folder)
        self.browse_button.pack(side=tk.LEFT)

        self.start_button = tk.Button(self.root, text="Start Scan", command=self.start_scan_thread)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self.root, text="Stop Scan", command=self.stop_scan)
        self.stop_button.pack(pady=5)

        self.wordlist_button = tk.Button(self.root, text="Select Wordlist", command=self.select_wordlist)
        self.wordlist_button.pack(pady=5)

        self.output_text = scrolledtext.ScrolledText(self.root, width=90, height=25)
        self.output_text.pack(pady=10)
        self.output_text.tag_config("hidden", foreground="green", font=("TkDefaultFont", 14))
        self.output_text.tag_config("error", foreground="red")

        self.wordlist_path = None
        self.log_file_path = os.path.join(os.path.dirname(__file__), "scan_log.txt")

    def drop(self, event):
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, event.data.strip('{}'))

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)

    def select_wordlist(self):
        self.wordlist_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.wordlist_path:
            self.log(f"[+] Wordlist selected: {self.wordlist_path}")

    def start_scan_thread(self):
        threading.Thread(target=self.start_scan, daemon=True).start()

    def stop_scan(self):
        self.stop_flag = True
        self.log("[!] Scan stopped")

    def log(self, message, tag=None):
        self.output_text.insert(tk.END, message + "\n", tag)
        self.output_text.see(tk.END)
        # فقط داده‌های مخفی رو توی فایل لاگ ثبت کن
        if tag == "hidden":
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                f.write(message + "\n")

    def analyze_file(self, file_path):
        self.log(f"\n=== Starting scan for file: {file_path} ===")

        file_type = magic.Magic(mime=True).from_file(file_path)
        self.log(f"[+] File type: {file_type}")

        if file_type.startswith('image'):
            self.extract_hidden_data(file_path)
            self.extract_exif(file_path)
            self.extract_ocr(file_path)

        if file_type == 'audio/mpeg':
            self.extract_mp3_metadata(file_path)

        self.calculate_hash(file_path)
        self.decode_base64(file_path)
        self.decrypt_classic_and_xor(file_path)
        self.analyze_hex_eof(file_path)

        if file_type in ['application/zip', 'application/x-rar-compressed'] and self.wordlist_path:
            self.brute_force_archive(file_path)

    def extract_hidden_data(self, file_path):
        try:
            secret = lsb.reveal(file_path)
            if secret:
                self.log(f"[+] Hidden LSB data found: {secret}", "hidden")
            else:
                self.log("[-] No hidden LSB data found")
        except Exception as e:
            self.log(f"[!] Error in LSB extraction: {e}", "error")

    def extract_exif(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f)
                if tags:
                    self.log("[+] EXIF data found:", "hidden")
                    for tag in tags.keys():
                        self.log(f"{tag}: {tags[tag]}", "hidden")
                else:
                    self.log("[-] No EXIF data found")
        except Exception as e:
            self.log(f"[!] Error in EXIF extraction: {e}", "error")

    def extract_ocr(self, file_path):
        try:
            img = Image.open(file_path).convert('L')
            img = img.point(lambda x: 0 if x < 128 else 255)
            text = pytesseract.image_to_string(img, lang='fas')
            if text.strip():
                self.log(f"[+] OCR text found: {text}", "hidden")
            else:
                self.log("[-] No OCR text found")
        except Exception as e:
            self.log(f"[!] Error in OCR extraction: {e}", "error")

    def extract_mp3_metadata(self, file_path):
        try:
            audio = MP3(file_path, ID3=EasyID3)
            if audio.tags:
                self.log("[+] MP3 metadata found:", "hidden")
                for key, value in audio.tags.items():
                    self.log(f"{key}: {value}", "hidden")
            else:
                self.log("[-] No MP3 metadata found")
        except Exception as e:
            self.log(f"[!] Error in MP3 metadata extraction: {e}", "error")

    def calculate_hash(self, file_path):
        try:
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            self.log(f"[+] SHA-256 hash: {sha256.hexdigest()}")
        except Exception as e:
            self.log(f"[!] Error in hash calculation: {e}", "error")

    def decode_base64(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                decoded = base64.b64decode(content)
                self.log("[+] Base64 decoded:", "hidden")
                self.log(decoded.decode('utf-8', errors='ignore'), "hidden")
        except Exception as e:
            self.log(f"[!] Error in Base64 decoding: {e}", "error")

    def decrypt_classic_and_xor(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                text = f.read().decode('utf-8', errors='ignore')
                if text.strip():
                    rot13 = text.encode().decode('rot_13')
                    caesar_shift = ''.join([chr(((ord(ch) - 65 + 3) % 26) + 65) if ch.isalpha() else ch for ch in text.upper()])
                    xor_key = 'X'
                    xor_decrypted = ''.join([chr(ord(c) ^ ord(xor_key)) for c in text])
                    self.log(f"[+] ROT13: {rot13}", "hidden")
                    self.log(f"[+] Caesar Shift (3): {caesar_shift}", "hidden")
                    self.log(f"[+] XOR (key '{xor_key}'): {xor_decrypted}", "hidden")
        except Exception as e:
            self.log(f"[!] Error in classic/XOR decryption: {e}", "error")

    def analyze_hex_eof(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                f.seek(-1024, os.SEEK_END) if os.path.getsize(file_path) > 1024 else f.seek(0)
                tail = f.read()
                hex_data = binascii.hexlify(tail).decode('ascii')
                if '504B0304' in hex_data:
                    self.log("[+] Hidden ZIP file found in EOF", "hidden")
                elif '52617221' in hex_data:
                    self.log("[+] Hidden RAR file found in EOF", "hidden")
                else:
                    self.log("[-] No hidden file found in EOF")
                self.log(f"[+] Hex data at EOF: {hex_data[:100]}...", "hidden")
        except Exception as e:
            self.log(f"[!] Error in EOF analysis: {e}", "error")

    def brute_force_archive(self, file_path):
        try:
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                wordlist = [line.strip() for line in f if line.strip()]
            total = len(wordlist)
            for i, pwd in enumerate(wordlist):
                if self.stop_flag:
                    return
                if i % 100 == 0 and self.stop_flag:
                    return
                progress = (i + 1) * 100 / total
                self.log(f"[*] Testing password {i + 1}/{total} ({progress:.2f}%): {pwd}")
                try:
                    if file_path.endswith('.zip'):
                        with zipfile.ZipFile(file_path) as zf:
                            zf.extractall(pwd=pwd.encode())
                            self.log(f"[+] ZIP password found: {pwd}", "hidden")
                            return
                    elif file_path.endswith('.rar'):
                        with rarfile.RarFile(file_path) as rf:
                            rf.extractall(pwd=pwd.encode())
                            self.log(f"[+] RAR password found: {pwd}", "hidden")
                            return
                except Exception:
                    continue
            self.log("[-] Archive password not found")
        except Exception as e:
            self.log(f"[!] Error in archive brute force: {e}", "error")

    def start_scan(self):
        self.stop_flag = False
        folder = self.folder_entry.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please enter a valid folder path")
            return
        self.output_text.delete(1.0, tk.END)
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)
        supported_extensions = ('.jpg', '.png', '.jpeg', '.mp3', '.zip', '.rar')
        for root, _, files in os.walk(folder):
            if self.stop_flag:
                return
            for file in files:
                if self.stop_flag:
                    return
                if file.lower().endswith(supported_extensions):
                    file_path = os.path.join(root, file)
                    self.analyze_file(file_path)
        if not self.stop_flag:
            self.log("[+] Scan completed!")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = SteganoExtractorApp(root)
    root.mainloop()
