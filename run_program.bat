@echo off
call env/Scripts/activate.bat & pip freeze & python python/LASplot.py
pause