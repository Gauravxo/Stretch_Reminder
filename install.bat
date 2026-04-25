@echo off
title Stretch Reminder - Install
color 0A

echo.
echo  ================================================
echo   STRETCH REMINDER - Windows 11 Setup
echo  ================================================
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found.
    echo Please install from https://python.org
    echo Check "Add Python to PATH" during install.
    pause & exit /b 1
)
python --version
echo.

echo Installing pystray and Pillow...
pip install pillow pystray --quiet --upgrade
echo Done.
echo.

set "DIR=%~dp0"
set "DIR=%DIR:~0,-1%"
set "PYW=%DIR%\stretch_reminder.pyw"
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"

echo Creating startup shortcut...
powershell -Command "$ws=New-Object -ComObject WScript.Shell; $sc=$ws.CreateShortcut('%STARTUP%\StretchReminder.lnk'); $sc.TargetPath='pythonw.exe'; $sc.Arguments='\"%PYW%\"'; $sc.WorkingDirectory='%DIR%'; $sc.Save()"
echo Startup shortcut: %STARTUP%\StretchReminder.lnk
echo.

echo Creating Desktop shortcut...
powershell -Command "$ws=New-Object -ComObject WScript.Shell; $sc=$ws.CreateShortcut('%USERPROFILE%\Desktop\Stretch Reminder.lnk'); $sc.TargetPath='pythonw.exe'; $sc.Arguments='\"%PYW%\"'; $sc.WorkingDirectory='%DIR%'; $sc.Save()"
echo.

echo Starting app now...
start "" pythonw.exe "%PYW%"
echo.

echo  ================================================
echo   DONE! App is running in your system tray.
echo   Right-click the tray icon (bottom-right).
echo.
echo   To TEST: right-click tray -> "Stretch NOW"
echo   To set 1-min test: edit config.json
echo     "interval_minutes": 1
echo  ================================================
echo.
pause
