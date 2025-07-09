@echo off
pyinstaller --noconfirm --clean --name "MnemonicHunter" ^
  --icon=mnemonic_hunter_icon.ico ^
  --add-data "resources;resources" ^
  --add-data "lang;lang" ^
  --add-data "output;output" ^
  --add-data "gui;gui" ^
  main.py
pause
