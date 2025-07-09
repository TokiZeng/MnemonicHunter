# MnemonicHunter/lang/__init__.py

import importlib
import os

def load_languages():
    languages = {}
    lang_path = os.path.dirname(__file__)
    for filename in os.listdir(lang_path):
        if filename.startswith("strings_") and filename.endswith(".py"):
            lang_code = filename[8:-3]  # 例如：strings_en.py → en
            module_name = f"lang.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "strings"):
                    languages[lang_code] = module.strings
            except Exception as e:
                print(f"[錯誤] 載入語言檔 {filename} 失敗：{e}")
    return languages
