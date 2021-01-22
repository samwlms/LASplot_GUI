@echo off
call python -m venv env & env\Scripts\activate.bat & env\Scripts\pip.exe install -r requirements.txt
pause