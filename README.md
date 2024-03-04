# iOS17-JIT-WIN
Enable JIT on iOS 17 using a windows PC  
tested on windows 11 with an ipad on 17.3.1
# SETUP
Install python and pymobiledevice3  
`pip install pymobiledevice3`  
Download/Clone jit_enabler_better.py into a working directory
Get a copy of llvm-mingw-20231128-msvcrt-x86_64 (https://github.com/mstorsjo/llvm-mingw/releases) and place the folder that directly contains "bin" into your working directory. 
# Usage
`python jit_enabler_better.py bundle_id`  
where bundle ID can be obtained e.g. inside AltStore under 'View App IDs'. If the correct one for your app doesn't show up, refresh your apps and try again.
