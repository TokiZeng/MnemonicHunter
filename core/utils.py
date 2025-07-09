import os
import re

# 判斷是否可能為錢包檔案
def is_wallet_file(filepath, content):
    wallet_keywords = [
        "wallet", "keystore", "bip39", "mnemonic", "seed", "recovery",
        "phrase", "xprv", "xpub", "passphrase", "restore", "electrum"
    ]
    noise_keywords = [
        "wikipedia", "film", "tv", "english", "zxcvbn", "us_tv", "frequency", 
        "common", "names", "passwords", "data", "search", "filtertrie"
    ]

    filename = os.path.basename(filepath).lower()
    content = content.lower()

    # 若 filename 含明顯雜訊關鍵詞，直接排除
    if any(nk in filename for nk in noise_keywords):
        return False

    # 關鍵詞出現次數統計（檔名 + 內容）
    match_count = sum(1 for kw in wallet_keywords if kw in filename or kw in content)

    return match_count >= 2  # 至少 2 個關鍵詞才視為錢包檔案


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
