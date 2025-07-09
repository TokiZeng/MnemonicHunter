# core/bip39_loader.py

import os
import sys

def get_resource_path(relative_path):
    """
    在 PyInstaller 打包後正確取得資源檔案的絕對路徑
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def load_bip39_words(path='resources/bip39_english.txt'):
    """
    載入 BIP39 詞表（每行一個單字）
    :param path: 詞表檔案的路徑（預設為內建詞表）
    :return: set 型態的單字集合
    """
    full_path = get_resource_path(path)

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            words = set(word.strip() for word in f if word.strip())
        return words
    except FileNotFoundError:
        print(f"[錯誤] 找不到詞表檔案：{full_path}")
        return set()
    except Exception as e:
        print(f"[錯誤] 載入詞表失敗：{e}")
        return set()
