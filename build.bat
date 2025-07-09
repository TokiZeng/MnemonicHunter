@echo off
pyinstaller --noconfirm --clean --name "MnemonicHunter" ^
  --add-data "resources;resources" ^
  --add-data "lang;lang" ^
  --add-data "output;output" ^
  --add-data "gui;gui" ^
  main.py
pause
