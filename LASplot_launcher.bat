@echo off

call :setESC

if exist env (
    call :lasplot_run
) else (
    call :lasplot_install
    call :lasplot_run
)

rem install program dependencies
:lasplot_install
ECHO %ESC%[95m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%ESC%[0m 
ECHO %ESC%[95m~~~~~~~~~~~%ESC%[0m %ESC%[93mLASplot Installer %ESC%[95m~~~~~~~~~~%ESC%[0m 
ECHO %ESC%[95m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%ESC%[0m 
ECHO %ESC%[96minitialising virtual environment...%ESC%[0m
call python -m venv env
call env\Scripts\activate.bat
ECHO %ESC%[96minstalling project dependencies...%ESC%[0m
call env\Scripts\pip.exe install -r requirements.txt 1>NUL 2>NUL
call env\Scripts\deactivate.bat
ECHO %ESC%[92minstall complete!%ESC%[0m
ECHO.
EXIT /B 0

rem run the LASplot program as normal
:lasplot_run 
ECHO %ESC%[95m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%ESC%[0m 
ECHO %ESC%[95m~~~~~~~~~~~~ %ESC%[93mLASplot Output%ESC%[0m %ESC%[95m~~~~~~~~~~~~%ESC%[0m 
ECHO %ESC%[95m~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~%ESC%[0m 
ECHO. 
env\Scripts\python.exe python\LASplot.py
EXIT /B 0


rem pretty colours!
:setESC
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set ESC=%%b
  exit /B 0
)
EXIT /B 0

pause