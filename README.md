

# 🧠 MnemonicHunter

A lightweight GUI tool to help you scan your local folders for files that may contain **cryptocurrency mnemonic phrases** (BIP39).  
Supports multiple languages, common document types, and a user-friendly interface with progress tracking.

---

## 🚀 Features

- 🔍 Scan for potential **mnemonic phrases** inside local files
- 📂 Supports common file types:
  - `.txt`
  - `.docx`
  - `.pdf`
  - `.xlsx`
- 🌐 Multi-language UI: Traditional Chinese, Japanese, Korean, English
- 📈 Progress bar, pause/resume, and cancel support
- ⚙️ Adjustable tolerance to allow typo flexibility

---

## ⚙️ Tolerance Explanation

You can define a **tolerance value** that allows a certain level of spelling deviation when searching for mnemonic words.

| Tolerance | Mode                |
|-----------|---------------------|
| `0`       | Strict match (exact) |
| `>0`      | Fuzzy match (allows typos) |

We recommend keeping it at `0` unless you suspect errors in the mnemonic input.

---

## 📦 How to Use

### ✅ Method 1: Use the pre-built `.exe` (Recommended)

1. Go to [Releases](https://github.com/TokiZeng/MnemonicHunter/releases)
2. Download `MnemonicHunter.zip` and extract it
3. Run `MnemonicHunter.exe` — **no installation needed**

---

## 📁 Project Structure

```
MnemonicHunter/
├── core/               # Scanning and logic
├── gui/                # Tkinter graphical interface
├── lang/               # Language files
├── resources/          # BIP39 wordlist
├── output/             # Scan result output (key.txt)
├── main.py             # Program entry point
├── build.bat           # Windows build script
├── mnemonic_hunter_icon.ico  # App icon
└── README.md
```

---

## 📄 Scan Results

After scanning, results are saved to:

```
output/key.txt
```

The file will contain paths to documents with suspected mnemonics or wallet-related content.

---

## 🙌 Contribution & Contact

Feel free to submit issues, pull requests, or help with translations!  
Author: [@TokiZeng](https://github.com/TokiZeng)



# 🧠 MnemonicHunter

一款專為幫助你搜尋電腦中可能包含加密貨幣助記詞（BIP39）的檔案而設計的簡單工具。  
內建 GUI 圖形介面，支援多語言，可掃描各種常見檔案格式並自動標示可疑項目。

---

## 🚀 功能特色

- 🔍 搜尋本機資料夾內可能包含 **助記詞（Mnemonic）** 的文件
- 📂 支援多種文件格式：
  - `.txt`
  - `.docx`
  - `.pdf`
  - `.xlsx`
- 🈳 支援多語言：繁體中文、日本語、한국어、English
- 📈 內建進度條與暫停／取消按鈕
- 🧠 可自訂容錯值（支援拼寫錯誤容忍）

---

## ⚙️ 容錯值（Tolerance）說明

在掃描時，你可以設定「容錯值」，用來容忍助記詞拼字上的誤差（例如多一個字母、少一個字母）。

| 容錯值 | 模式說明         |
|--------|------------------|
| `0`    | 嚴格匹配（完全一致） |
| `>0`   | 寬鬆匹配（允許拼寫偏差） |

建議預設使用 `0`，若需容忍人為輸入錯誤可設為 1~3。

---

## 📦 下載與使用方式

### ✅ 方法一：直接執行 `.exe`（推薦）

1. 前往 [Releases](https://github.com/TokiZeng/MnemonicHunter/releases)
2. 下載 `MnemonicHunter.zip` 並解壓縮
3. 執行 `MnemonicHunter.exe` 即可開始使用（**免安裝**）

---

## 📁 專案結構簡介

```
MnemonicHunter/
├── core/               # 掃描與邏輯處理
├── gui/                # Tkinter 圖形介面
├── lang/               # 多語言介面文字
├── resources/          # BIP39 詞表檔案
├── output/             # 掃描結果輸出（key.txt）
├── main.py             # 程式進入點
├── build.bat           # Windows 一鍵打包腳本
├── mnemonic_hunter_icon.ico  # 專案圖示
└── README.md
```

---

## 📄 掃描結果

掃描結束後會將結果儲存在：
```
output/key.txt
```
可疑助記詞或錢包檔案路徑都會顯示在該檔案中。

---

## 🙌 聯絡與貢獻

歡迎 issue、pull request 或提供語言翻譯與功能建議！  
作者：[@TokiZeng](https://github.com/TokiZeng)
