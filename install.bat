powershell -command "& { (New-Object Net.WebClient).DownloadFile('https://github.com/mstorsjo/llvm-mingw/releases/download/20231128/llvm-mingw-20231128-msvcrt-x86_64.zip', 'archive.zip') }"
tar -xf archive.zip
del archive.zip
pip install pymobiledevice3