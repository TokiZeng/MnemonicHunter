import os
import re

# 判斷是否可能為錢包檔案
def is_wallet_file(filepath, content):
    wallet_keywords = [
        "wallet.dat", "keystore", "UTC--", "xprv", "xpub",
        "mnemonic", "bip39", "electrum", "seed", "passphrase"
    ]
    filename = os.path.basename(filepath).lower()
    content = content.lower()

    for keyword in wallet_keywords:
        if keyword in filename or keyword in content:
            return True
    return False

# 取得絕對路徑（支援相對或使用者目錄）
def resolve_path(path):
    return os.path.abspath(os.path.expanduser(path))

def count_target_files(directory, target_exts={'.txt', '.docx', '.pdf', '.xlsx'}):
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if os.path.splitext(file)[1].lower() in target_exts:
                count += 1
    return count

def save_results(results, output_path="output/key.txt"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for line in results:
            f.write(line + "\n")
