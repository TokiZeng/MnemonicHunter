import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import threading
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
        self.root.geometry("500x580")

        self.selected_directory = tk.StringVar()
        self.scanning = False
        self.paused = False
        self.stop_requested = False
        self.thread = None

        self.tolerance = tk.StringVar(value="0")

        # 語言選單
        self.menu_bar = tk.Menu(self.root)
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        for code in self.languages:
            self.language_menu.add_command(label=code, command=lambda c=code: self.change_language(c))
        self.menu_bar.add_cascade(label="Language", menu=self.language_menu)
        self.root.config(menu=self.menu_bar)

        # 資料夾選擇
        self.label_select = tk.Label(root, text=self.lang["select_directory"])
        self.label_select.pack(anchor="w", padx=10, pady=(10, 0))

        frame = tk.Frame(root)
        frame.pack(fill="x", padx=10)
        self.entry = tk.Entry(frame, textvariable=self.selected_directory)
        self.entry.pack(side="left", fill="x", expand=True)
        self.browse_button = tk.Button(frame, text=self.lang["browse"], command=self.browse_directory)
        self.browse_button.pack(side="left")

        # 容錯輸入欄位
        self.tolerance_label = tk.Label(root, text=self.lang["tolerance_hint"])
        self.tolerance_label.pack(anchor="w", padx=10)
        self.tolerance_entry = tk.Entry(root, textvariable=self.tolerance)
        self.tolerance_entry.pack(fill="x", padx=10, pady=(0, 10))

        self.scan_button = tk.Button(root, text=self.lang["simple_search"], command=self.toggle_scan)
        self.scan_button.pack(pady=10)

        self.progress_label = tk.Label(root, text=self.lang["progress"])
        self.progress_label.pack(anchor="w", padx=10)
        self.progress = ttk.Progressbar(root, length=400, mode="determinate")
        self.progress.pack(pady=5)

        self.progress_percent_label = tk.Label(root, text="0%")
        self.progress_percent_label.pack(anchor="w", padx=10)

        self.current_file_label = tk.Label(root, text="")
        self.current_file_label.pack(anchor="w", padx=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        self.pause_button = tk.Button(btn_frame, text=self.lang["pause"], command=self.toggle_pause)
        self.pause_button.pack(side="left", padx=5)

        self.cancel_button = tk.Button(btn_frame, text=self.lang["cancel"], command=self.cancel_scan, state="disabled")
        self.cancel_button.pack(side="left", padx=5)

        self.status_label = tk.Label(root, text=self.lang["status_idle"])
        self.status_label.pack(pady=(5, 10))

        self.output_text = tk.Text(root, height=8, wrap="none")
        self.output_text.pack(fill="both", padx=10, pady=(0, 10), expand=True)

    def change_language(self, lang_code):
        if lang_code in self.languages:
            self.current_lang = lang_code
            self.lang = self.languages[lang_code]
            self.update_texts()

    def update_texts(self):
        self.root.title(self.lang["title"])
        self.label_select.config(text=self.lang["select_directory"])
        self.browse_button.config(text=self.lang["browse"])
        self.tolerance_label.config(text=self.lang["tolerance_hint"])
        self.scan_button.config(text=self.lang["simple_search"])
        self.progress_label.config(text=self.lang["progress"])
        self.pause_button.config(text=self.lang["pause"])
        self.cancel_button.config(text=self.lang["cancel"])
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
        self.output_text.delete(1.0, tk.END)
        self.progress["value"] = 0
        self.progress_percent_label.config(text="0%")
        self.current_file_label.config(text="")
        self.scanning = True
        self.stop_requested = False
        self.cancel_button.config(state="normal")
        self.status_label.config(text=self.lang["status_scanning"])
        self.thread = threading.Thread(target=self.run_scan)
        self.thread.start()

    def toggle_pause(self):
        if self.scanning:
            self.paused = not self.paused
            new_text = self.lang["resume"] if self.paused else self.lang["pause"]
            self.pause_button.config(text=new_text)

    def cancel_scan(self):
        self.stop_requested = True
        self.status_label.config(text=self.lang["status_cancelled"])

    def run_scan(self):
        directory = self.selected_directory.get()
        results = []

        try:
            tolerance = int(self.tolerance.get())
            if tolerance < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(self.lang["error_title"], self.lang["tolerance_error"])
            self.scanning = False
            return

        mode = "strict" if tolerance == 0 else "tolerant"
        scanner_instance = scanner.MnemonicScanner(
            bip39_path="resources/bip39_english.txt",
            mode=mode,
            tolerance=tolerance
        )

        total_files = utils.count_target_files(directory)
        scanned = 0

        def update_progress(current_file):
            nonlocal scanned
            if self.stop_requested:
                raise Exception("Scan cancelled")
            scanned += 1
            percent = int((scanned / total_files) * 100)
            self.progress["value"] = percent
            self.progress_percent_label.config(text=f"{percent}%")
            self.current_file_label.config(text=f"{self.lang['scanning']}: {current_file}")
            self.root.update_idletasks()
            while self.paused:
                self.status_label.config(text=self.lang["pause"])
                self.root.update()
                if self.stop_requested:
                    raise Exception("Scan cancelled")

        try:
            scan_results = scanner_instance.scan_directory(directory, callback=update_progress)
            for item in scan_results:
                if self.stop_requested:
                    raise Exception("Scan cancelled")
                if item["mnemonic_count"] > 0:
                    line = f"{item['path']}：{item['mnemonic_count']} {self.lang['mnemonic_found']}"
                    results.append(line)
                    self.output_text.insert(tk.END, line + "\n")
                elif item["is_wallet"]:
                    line = f"{item['path']}：{self.lang['wallet_found']}"
                    results.append(line)
                    self.output_text.insert(tk.END, line + "\n")
            if not self.stop_requested:
                utils.save_results(results)
                self.status_label.config(text=self.lang["status_done"])
                messagebox.showinfo(self.lang["title"], self.lang["output_saved"])
        except Exception:
            self.output_text.insert(tk.END, f"\n{self.lang['cancel_notice']}\n")
            self.status_label.config(text=self.lang["status_cancelled"])
        finally:
            self.scanning = False
            self.paused = False
            self.stop_requested = False
            self.progress["value"] = 0
            self.progress_percent_label.config(text="0%")
            self.cancel_button.config(state="disabled")
            self.pause_button.config(text=self.lang["pause"])
            self.current_file_label.config(text="")

def main():
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

def run_gui():
    main()
