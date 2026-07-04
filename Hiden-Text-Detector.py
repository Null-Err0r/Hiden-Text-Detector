#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
import pytesseract
from stegano import lsb
import exifread
import base64
import hashlib
import binascii
import magic
import threading
import queue
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import zipfile
import rarfile

class SteganoExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hidden Text Detector - Pro Edition")
        self.root.geometry("850x700")
        self.stop_flag = threading.Event()
        self.log_queue = queue.Queue()

        self.setup_ui()
        self.wordlist_path = None
        self.log_file_path = os.path.join(os.path.dirname(__file__), "scan_log.txt")
        
        # Start queue processing
        self.root.after(100, self.process_queue)

    def setup_ui(self):
        # Top Frame for folder selection
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10, fill=tk.X, padx=20)

        tk.Label(self.top_frame, text="Target Folder:").pack(side=tk.LEFT)
        self.folder_entry = tk.Entry(self.top_frame, width=50)
        self.folder_entry.pack(side=tk.LEFT, padx=10, expand=True, fill=tk.X)
        self.folder_entry.drop_target_register(DND_FILES)
        self.folder_entry.dnd_bind('<<Drop>>', self.drop)

        self.browse_button = tk.Button(self.top_frame, text="Browse", command=self.browse_folder)
        self.browse_button.pack(side=tk.LEFT)

        # Controls Frame
        self.controls_frame = tk.Frame(self.root)
        self.controls_frame.pack(pady=5, fill=tk.X, padx=20)

        self.wordlist_button = tk.Button(self.controls_frame, text="Select Wordlist", command=self.select_wordlist)
        self.wordlist_button.pack(side=tk.LEFT, padx=5)

        self.start_button = tk.Button(self.controls_frame, text="Start Scan", command=self.start_scan_thread, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.controls_frame, text="Stop Scan", command=self.stop_scan, bg="red", fg="white")
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_label = tk.Label(self.controls_frame, textvariable=self.status_var, fg="blue")
        self.status_label.pack(side=tk.LEFT, padx=20)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=5, fill=tk.X, padx=20)

        # Output text
        self.output_text = scrolledtext.ScrolledText(self.root, width=90, height=25)
        self.output_text.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        self.output_text.tag_config("hidden", foreground="green", font=("TkDefaultFont", 12, "bold"))
        self.output_text.tag_config("error", foreground="red")
        self.output_text.tag_config("info", foreground="blue")

    def drop(self, event):
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, event.data.strip('{}'))

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)

    def select_wordlist(self):
        self.wordlist_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.wordlist_path:
            self.enqueue_log(f"[+] Wordlist selected: {self.wordlist_path}", "info")

    def enqueue_log(self, message, tag=None):
        self.log_queue.put(("log", message, tag))
        
    def enqueue_status(self, status, progress=None):
        self.log_queue.put(("status", status, progress))

    def process_queue(self):
        try:
            while True:
                item = self.log_queue.get_nowait()
                if item[0] == "log":
                    msg, tag = item[1], item[2]
                    self.output_text.insert(tk.END, msg + "\n", tag)
                    self.output_text.see(tk.END)
                    if tag == "hidden":
                        try:
                            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                                f.write(msg + "\n")
                        except Exception:
                            pass
                elif item[0] == "status":
                    status_text, prog = item[1], item[2]
                    if status_text is not None:
                        self.status_var.set(status_text)
                    if prog is not None:
                        self.progress_var.set(prog)
                elif item[0] == "clear":
                    self.output_text.delete(1.0, tk.END)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_queue)

    def start_scan_thread(self):
        if not self.stop_flag.is_set() and self.status_var.get() != "Ready" and self.status_var.get() != "Scan completed!" and self.status_var.get() != "Scan stopped":
            messagebox.showwarning("Warning", "Scan is already running!")
            return
            
        folder = self.folder_entry.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showerror("Error", "Please enter a valid folder path")
            return
            
        self.stop_flag.clear()
        self.log_queue.put(("clear", None, None))
        
        # Clear log file
        try:
            if os.path.exists(self.log_file_path):
                os.remove(self.log_file_path)
        except Exception:
            pass

        threading.Thread(target=self.scan_worker, args=(folder,), daemon=True).start()

    def stop_scan(self):
        self.stop_flag.set()
        self.enqueue_status("Stopping scan...")

    def scan_worker(self, folder):
        supported_extensions = ('.jpg', '.png', '.jpeg', '.mp3', '.zip', '.rar', '.txt')
        
        files_to_scan = []
        for root_dir, _, files in os.walk(folder):
            for file in files:
                if file.lower().endswith(supported_extensions):
                    files_to_scan.append(os.path.join(root_dir, file))
                    
        total_files = len(files_to_scan)
        if total_files == 0:
            self.enqueue_log("[-] No supported files found in the directory.", "info")
            self.enqueue_status("Scan completed!", 100)
            return

        for idx, file_path in enumerate(files_to_scan):
            if self.stop_flag.is_set():
                break
                
            progress = (idx / total_files) * 100
            self.enqueue_status(f"Scanning: {os.path.basename(file_path)}", progress)
            self.analyze_file(file_path)

        if self.stop_flag.is_set():
            self.enqueue_log("[!] Scan stopped by user", "info")
            self.enqueue_status("Scan stopped")
        else:
            self.enqueue_log("[+] Scan completed!", "info")
            self.enqueue_status("Scan completed!", 100)

    def analyze_file(self, file_path):
        self.enqueue_log(f"\n=== Starting scan for file: {file_path} ===")

        try:
            file_type = magic.Magic(mime=True).from_file(file_path)
            self.enqueue_log(f"[+] File type: {file_type}")
        except Exception as e:
            file_type = "unknown"
            self.enqueue_log(f"[-] Could not determine file type: {e}", "error")

        if file_type.startswith('image'):
            self.extract_hidden_data(file_path)
            self.extract_exif(file_path)
            self.extract_ocr(file_path)

        if file_type == 'audio/mpeg' or file_path.lower().endswith('.mp3'):
            self.extract_mp3_metadata(file_path)

        self.calculate_hash(file_path)
        
        # Apply text-based decryptions to all files, but extract strings safely first
        self.decode_base64(file_path)
        self.decrypt_classic_and_xor(file_path)

        self.analyze_hex_eof(file_path)

        if (file_type in ['application/zip', 'application/x-rar-compressed'] or file_path.lower().endswith(('.zip', '.rar'))) and self.wordlist_path:
            self.brute_force_archive(file_path)

    def extract_hidden_data(self, file_path):
        try:
            secret = lsb.reveal(file_path)
            if secret:
                self.enqueue_log(f"[+] Hidden LSB data found: {secret}", "hidden")
            else:
                self.enqueue_log("[-] No hidden LSB data found")
        except IndexError:
            self.enqueue_log("[-] No hidden LSB data found (IndexError)")
        except Exception as e:
            self.enqueue_log(f"[!] Error in LSB extraction: {e}", "error")

    def extract_exif(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f)
                if tags:
                    self.enqueue_log("[+] EXIF data found:", "hidden")
                    for tag in tags.keys():
                        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
                            self.enqueue_log(f"    {tag}: {tags[tag]}", "hidden")
                else:
                    self.enqueue_log("[-] No EXIF data found")
        except Exception as e:
            self.enqueue_log(f"[!] Error in EXIF extraction: {e}", "error")

    def extract_ocr(self, file_path):
        try:
            img = Image.open(file_path).convert('L')
            img = img.point(lambda x: 0 if x < 128 else 255)
            text = pytesseract.image_to_string(img, lang='fas+eng')
            if text.strip():
                self.enqueue_log(f"[+] OCR text found:\n{text.strip()}", "hidden")
            else:
                self.enqueue_log("[-] No OCR text found")
        except Exception as e:
            self.enqueue_log(f"[!] Error in OCR extraction: {e}. (Ensure Tesseract is installed)", "error")

    def extract_mp3_metadata(self, file_path):
        try:
            audio = MP3(file_path, ID3=EasyID3)
            if audio.tags:
                self.enqueue_log("[+] MP3 metadata found:", "hidden")
                for key, value in audio.tags.items():
                    self.enqueue_log(f"    {key}: {value}", "hidden")
            else:
                self.enqueue_log("[-] No MP3 metadata found")
        except Exception as e:
            self.enqueue_log(f"[!] Error in MP3 metadata extraction: {e}", "error")

    def calculate_hash(self, file_path):
        try:
            sha256 = hashlib.sha256()
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            self.enqueue_log(f"[+] SHA-256 hash: {sha256.hexdigest()}")
        except Exception as e:
            self.enqueue_log(f"[!] Error in hash calculation: {e}", "error")

    def get_text_content(self, file_path):
        import re
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            # If it's small enough, try treating it as UTF-8 entirely
            try:
                return [data.decode('utf-8')]
            except UnicodeDecodeError:
                pass
                
            # If it's a binary file, extract printable ASCII strings
            strings = re.findall(b'[ -~]{5,}', data)
            return [s.decode('ascii') for s in strings if len(s) > 5]
        except Exception:
            return []

    def decode_base64(self, file_path):
        try:
            import re
            contents = self.get_text_content(file_path)
            b64_pattern = re.compile(r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')
            
            found_b64 = False
            for content in contents:
                if not content.strip(): continue
                for match in b64_pattern.findall(content):
                    try:
                        decoded = base64.b64decode(match).decode('utf-8')
                        if decoded.isprintable() and len(decoded) > 3:
                            self.enqueue_log(f"[+] Base64 decoded:\n{decoded}", "hidden")
                            found_b64 = True
                    except Exception:
                        pass
            if not found_b64:
                self.enqueue_log("[-] No Base64 data found")
        except Exception as e:
            self.enqueue_log(f"[!] Error in Base64 decoding: {e}", "error")

    def decrypt_classic_and_xor(self, file_path):
        try:
            import codecs
            contents = self.get_text_content(file_path)
            
            rot13_results = []
            caesar_results = []
            
            for text in contents:
                text = text.strip()
                if not text or len(text) > 1000: # Skip huge chunks to avoid UI lag
                    continue
                    
                # ROT13
                rot13 = codecs.encode(text, 'rot_13')
                if rot13 != text:
                    rot13_results.append(rot13)
                    
                # Caesar Shift 3
                caesar_shift = ''.join([chr(((ord(ch) - 65 + 3) % 26) + 65) if 'A' <= ch <= 'Z' else (chr(((ord(ch) - 97 + 3) % 26) + 97) if 'a' <= ch <= 'z' else ch) for ch in text])
                if caesar_shift != text:
                    caesar_results.append(caesar_shift)

            if rot13_results:
                self.enqueue_log(f"[+] ROT13 possible texts (snippet): {rot13_results[0][:100]}...", "hidden")
            if caesar_results:
                self.enqueue_log(f"[+] Caesar Shift 3 possible texts (snippet): {caesar_results[0][:100]}...", "hidden")

            # XOR - byte-wise on the whole file using key 'X'
            with open(file_path, 'rb') as f:
                data = f.read()
            xor_key = ord('X')
            xored_data = bytes([b ^ xor_key for b in data])
            import re
            strings = re.findall(b'[ -~]{5,}', xored_data)
            xor_decrypted = [s.decode('ascii') for s in strings if len(s) > 5]
            
            if xor_decrypted:
                self.enqueue_log(f"[+] XOR (key 'X') possible texts (snippet): {xor_decrypted[0][:100]}...", "hidden")
                
        except Exception as e:
            self.enqueue_log(f"[!] Error in classic/XOR decryption: {e}", "error")

    def analyze_hex_eof(self, file_path):
        try:
            with open(file_path, 'rb') as f:
                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    return
                
                chunk_size = min(1024, file_size)
                f.seek(-chunk_size, os.SEEK_END)
                tail = f.read()
                
                if b'PK\x03\x04' in tail:
                    self.enqueue_log("[+] Hidden ZIP file found in EOF", "hidden")
                elif b'Rar!\x1a\x07' in tail:
                    self.enqueue_log("[+] Hidden RAR file found in EOF", "hidden")
                else:
                    self.enqueue_log("[-] No hidden ZIP/RAR file found in EOF bytes")
        except Exception as e:
            self.enqueue_log(f"[!] Error in EOF analysis: {e}", "error")

    def get_wordlist_size(self):
        try:
            with open(self.wordlist_path, 'rb') as f:
                return sum(1 for _ in f)
        except:
            return 0

    def brute_force_archive(self, file_path):
        self.enqueue_log(f"[*] Starting brute force on {os.path.basename(file_path)}")
        self.enqueue_status(f"Counting wordlist lines...")
        
        total_words = self.get_wordlist_size()
        if total_words == 0:
            self.enqueue_log("[-] Wordlist is empty or inaccessible.", "error")
            return

        is_zip = file_path.lower().endswith('.zip')
        is_rar = file_path.lower().endswith('.rar')
        
        archive_obj = None
        try:
            if is_zip:
                archive_obj = zipfile.ZipFile(file_path)
            elif is_rar:
                archive_obj = rarfile.RarFile(file_path)
        except Exception as e:
            self.enqueue_log(f"[!] Failed to open archive: {e}", "error")
            return

        try:
            with open(self.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f):
                    if self.stop_flag.is_set():
                        self.enqueue_log("[-] Brute force aborted by user.")
                        break
                        
                    pwd = line.strip()
                    if not pwd:
                        continue
                        
                    if i % 100 == 0:
                        progress = (i / total_words) * 100
                        self.enqueue_status(f"Brute-forcing: {pwd}", progress)
                        
                    try:
                        if is_zip:
                            archive_obj.extractall(pwd=pwd.encode('utf-8'))
                            self.enqueue_log(f"[+] ZIP password found: {pwd}", "hidden")
                            return
                        elif is_rar:
                            archive_obj.extractall(pwd=pwd.encode('utf-8'))
                            self.enqueue_log(f"[+] RAR password found: {pwd}", "hidden")
                            return
                    except (RuntimeError, zipfile.BadZipFile, rarfile.Error, Exception):
                        continue
                        
            if not self.stop_flag.is_set():
                self.enqueue_log("[-] Archive password not found in wordlist")
        except Exception as e:
            self.enqueue_log(f"[!] Error during brute force: {e}", "error")
        finally:
            if archive_obj:
                archive_obj.close()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = SteganoExtractorApp(root)
    root.mainloop()
