@echo off
title Stretch Reminder - Uninstall
taskkill /f /im pythonw.exe >nul 2>&1
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
if exist "%STARTUP%\StretchReminder.lnk" del "%STARTUP%\StretchReminder.lnk" && echo Startup shortcut removed.
if exist "%USERPROFILE%\Desktop\Stretch Reminder.lnk" del "%USERPROFILE%\Desktop\Stretch Reminder.lnk" && echo Desktop shortcut removed.
echo Done.
pause
