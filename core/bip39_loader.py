# core/bip39_loader.py

def load_bip39_words(path='resources/bip39_english.txt'):
    """
    載入 BIP39 詞表（每行一個單字）
    :param path: 詞表檔案的路徑
    :return: set 型態的單字集合
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            words = set(word.strip() for word in f if word.strip())
        return words
    except FileNotFoundError:
        print(f"[錯誤] 找不到詞表檔案：{path}")
        return set()
    except Exception as e:
        print(f"[錯誤] 載入詞表失敗：{e}")
        return set()
