@echo off
ECHO ------------------------LASPLOT INSTALLATION------------------------------
ECHO installing project dependencies and initialising virtual environment...
call python -m venv env & env\Scripts\activate.bat & env\Scripts\pip.exe install -r requirements.txt