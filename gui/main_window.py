import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
import os
from core import scanner
from core import bip39_loader
from core import utils
from lang import load_languages

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.languages = load_languages()
        self.current_lang = list(self.languages.keys())[0]
        self.lang = self.languages[self.current_lang]

        self.root.title(self.lang["title"])
        self.root.geometry("500x450")

        self.selected_directory = tk.StringVar()
        self.scanning = False
        self.paused = False
        self.thread = None

        # 語言選單
        self.menu_bar = tk.Menu(self.root)
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        for code in self.languages:
            label = code  # 顯示語言代碼，如 "en", "zh"
            self.language_menu.add_command(label=label, command=lambda c=code: self.change_language(c))
        self.menu_bar.add_cascade(label="Language", menu=self.language_menu)
        self.root.config(menu=self.menu_bar)

        # GUI 元件
        self.label_select = tk.Label(root, text=self.lang["select_directory"])
        self.label_select.pack(anchor="w", padx=10, pady=(10, 0))

        frame = tk.Frame(root)
        frame.pack(fill="x", padx=10)
        self.entry = tk.Entry(frame, textvariable=self.selected_directory)
        self.entry.pack(side="left", fill="x", expand=True)
        self.browse_button = tk.Button(frame, text="...", command=self.browse_directory, width=4)
        self.browse_button.pack(side="left")

        self.scan_button = tk.Button(root, text=self.lang["simple_search"], command=self.toggle_scan)
        self.scan_button.pack(pady=10)

        self.progress_label = tk.Label(root, text=self.lang["progress"])
        self.progress_label.pack(anchor="w", padx=10)
        self.progress = ttk.Progressbar(root, length=400, mode="determinate")
        self.progress.pack(pady=5)

        self.pause_button = tk.Button(root, text=self.lang["pause"], command=self.toggle_pause)
        self.pause_button.pack(pady=5)

        self.status_label = tk.Label(root, text=self.lang["status_idle"])
        self.status_label.pack(pady=(5, 10))

    def change_language(self, lang_code):
        if lang_code in self.languages:
            self.current_lang = lang_code
            self.lang = self.languages[lang_code]
            self.update_texts()

    def update_texts(self):
        self.root.title(self.lang["title"])
        self.label_select.config(text=self.lang["select_directory"])
        self.scan_button.config(text=self.lang["simple_search"])
        self.progress_label.config(text=self.lang["progress"])
        self.pause_button.config(text=self.lang["pause"])
        self.status_label.config(text=self.lang["status_idle"])

    def browse_directory(self):
        path = filedialog.askdirectory()
        if path:
            self.selected_directory.set(path)

    def toggle_scan(self):
        if not self.selected_directory.get():
            messagebox.showwarning(self.lang["title"], self.lang["no_folder_selected"])
            return
        if self.scanning:
            return
        self.scanning = True
        self.status_label.config(text=self.lang["status_scanning"])
        self.thread = threading.Thread(target=self.run_scan)
        self.thread.start()

    def toggle_pause(self):
        if self.scanning:
            self.paused = not self.paused
            new_text = self.lang["resume"] if self.paused else self.lang["pause"]
            self.pause_button.config(text=new_text)

    def run_scan(self):
        directory = self.selected_directory.get()
        results = []

        # 建立 MnemonicScanner 實例
        scanner_instance = scanner.MnemonicScanner(bip39_path="resources/bip39_english.txt")

        total_files = utils.count_target_files(directory)
        scanned = 0

        def update_progress(_):
            nonlocal scanned
            scanned += 1
            self.progress["value"] = (scanned / total_files) * 100
            self.root.update_idletasks()
            while self.paused:
                self.status_label.config(text=self.lang["pause"])
                self.root.update()

        scan_results = scanner_instance.scan_directory(directory, callback=update_progress)

        for item in scan_results:
            if item["mnemonic_count"] > 0:
                results.append(f"{item['path']}：{item['mnemonic_count']} {self.lang['mnemonic_found']}")
            elif item["is_wallet"]:
                results.append(f"{item['path']}：{self.lang['wallet_found']}")

        utils.save_results(results)
        self.status_label.config(text=self.lang["status_done"])
        messagebox.showinfo(self.lang["title"], self.lang["output_saved"])
        self.scanning = False


def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

def run_gui():
    main()
