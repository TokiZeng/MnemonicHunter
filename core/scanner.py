import os
import re
import docx
import pdfplumber
import openpyxl
from mnemonic import Mnemonic

from core.bip39_loader import load_bip39_words
from core.utils import is_wallet_file

class MnemonicScanner:
    def __init__(self, bip39_path, mode='strict', tolerance=5):
        self.bip39_words = load_bip39_words(bip39_path)
        self.bip39_set = set(self.bip39_words)
        self.mnemo = Mnemonic("english")
        self.target_exts = {'.txt', '.docx', '.pdf', '.xlsx'}
        self.exclude_files = {
            os.path.abspath('output/key.txt'),
            os.path.abspath('resources/bip39_english.txt')
        }
        self.mode = mode
        self.tolerance = tolerance

    def extract_text(self, filepath):
        ext = os.path.splitext(filepath)[1].lower()
        try:
            if ext == ".txt":
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()
            elif ext == ".docx":
                doc = docx.Document(filepath)
                return "\n".join(p.text for p in doc.paragraphs)
            elif ext == ".pdf":
                with pdfplumber.open(filepath) as pdf:
                    return "\n".join(page.extract_text() or "" for page in pdf.pages)
            elif ext == ".xlsx":
                wb = openpyxl.load_workbook(filepath, data_only=True)
                text = []
                for sheet in wb.worksheets:
                    for row in sheet.iter_rows():
                        for cell in row:
                            if cell.value:
                                text.append(str(cell.value))
                return "\n".join(text)
        except Exception:
            return ""
        return ""

    def scan_file(self, filepath):
        text = self.extract_text(filepath).lower()
        words = re.findall(r'\b[a-z]+\b', text)

        bip39_words = [word for word in words if word in self.bip39_set]
        non_bip39_count = len(words) - len(bip39_words)

        if self.mode == 'strict' and non_bip39_count > 0:
            return None
        elif self.mode == 'tolerant' and non_bip39_count > self.tolerance:
            return None

        if len(bip39_words) in {12, 15, 18, 21, 24}:
            phrase = ' '.join(bip39_words)
            if self.mnemo.check(phrase):
                return {
                    "path": filepath,
                    "mnemonic_count": len(bip39_words),
                    "is_wallet": is_wallet_file(filepath, text)
                }

        return None

    def scan_directory(self, base_path, callback=None):
        results = []
        for root, _, files in os.walk(base_path):
            for file in files:
                filepath = os.path.join(root, file)

                if (
                    os.path.splitext(filepath)[1].lower() not in self.target_exts
                    or os.path.abspath(filepath) in self.exclude_files
                ):
                    continue

                if callback:
                    callback(filepath)

                res = self.scan_file(filepath)
                if res:
                    results.append(res)
        return results
