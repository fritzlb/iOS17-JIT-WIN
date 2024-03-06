set "params=%*"
cd /d "%~dp0" && ( if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs" ) && fsutil dirty query %systemdrive% 1>nul 2>nul || (  echo Set UAC = CreateObject^("Shell.Application"^) : UAC.ShellExecute "cmd.exe", "/k cd ""%~sdp0"" && ""%~s0"" %params%", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && exit /B )

powershell -command "& { (New-Object Net.WebClient).DownloadFile('https://github.com/mstorsjo/llvm-mingw/releases/download/20231128/llvm-mingw-20231128-msvcrt-x86_64.zip', 'archive.zip') }"
tar -xf archive.zip
del archive.zip
pip install pymobiledevice3


@echo off
setlocal enabledelayedexpansion

set "message=For everything to work, it is recommended to reboot the PC now. Do you want to reboot?"
set "title=Reboot recommended"

echo Set objShell = CreateObject("WScript.Shell") > "%temp%\messagebox.vbs"
echo result = objShell.Popup("%message%", 0, "%title%", 36) >> "%temp%\messagebox.vbs"
echo WScript.Quit(result) >> "%temp%\messagebox.vbs"

cscript //nologo "%temp%\messagebox.vbs"
set "result=%errorlevel%"

del "%temp%\messagebox.vbs"

if !result! equ 6 (
    echo Rebooting...
    shutdown /r /t 0
) else (
    exit
)

endlocal
