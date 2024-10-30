# Warning: better alternatives
SideJITserver does the same, but even better. It supports WiFi connections, this project does not. Please consider using that instead of this collection of scripts.  

# iOS17-JIT-WIN
Enable JIT on iOS 17 using a windows PC 
  
Video guide: https://youtu.be/MLHa2JLuk3Y  
  
Tested with Windows 11 and iOS 17.3.1 as well as 17.4.  
The following apps have been tested by me and do work:
- PojavLauncher (pay attention to the tips section down below!)
- UTM (AltStore release version)
- DolphiniOS (pay attention to the tips section down below!)

# Requirements
- Windows 11 PC (probably a more or less recent (v2004+, from 2020+) build of windows 10 works too, I didn't test that)
- iOS device running iOS 17+
- Sideloaded App requiring JIT that's been sideloaded using a supported method (AltStore, Sideloadly, other methods using developer certificates)

# SETUP
Install python 3.12.2 from https://www.python.org/downloads/release/python-3122/. Make sure to add it to your PATH.  
Download/Clone this repo (green button -> download zip), extract the zip whereever you'd like and run install.bat by double clicking it.  

# MacOS SETUP
Initial macOS support added by @axeleszu

Install Xcode Command line tools.
  
Then run the following commands, one by one:    
```  
python3 -m venv venv
. ./venv/bin/activate  
pip install pymobiledevice3==2.46.2  
pip install qh3==0.15.1  
```  

# Usage (Windows)
Make sure to log in as admin.  
Open an admin terminal by double clicking "open terminal here.bat".  
Run `python jit_enabler_better.py {bundle_id}` by typing it into the terminal window and finish the command by pressing enter.  
Make sure to replace {bundle_ID} with your actual bundle ID, which can be obtained e.g. inside AltStore under 'View App IDs'. If the correct one for your app doesn't show up, refresh your apps and try again.  
If you're using sideloadly, you can set a custom bundle ID to make things easy for you. You'll find the according settings under "advanced".  
Be aware that simply googling the bundle ID will not work because your sideloding software will modify it. This is because every bundle ID gets registered with Apple and then belongs to that particular Xcode team, therefore it can't be used by anyone else. 

# MacOS Usage
`sudo python jit_enabler_better-mac.py {bundle_id}`

# Issues
If you do experience issues with this, please run the script in debug mode and create an issue with the terminal output. To start in debug mode, simply add "True" as another argument to the command, like this:  
`python jit_enabler_better.py {bundle_id} True` replacing {bundle_id} with your bundle ID of course. :)  
Here are some common troubleshooting tips though:  
- Reboot your PC. Use the restart button, shutting down and starting again isn't the same.
- If there's an error like "Python was not found" follow the installation instructions and install python.
- If there's an error like "pymobiledevice3 not found", you probably forgot executing install.bat. Do that (again).
- If you get an error while running debug commands (usually sth like file not found), try executing install_slow.bat. It'll redownload everything and use a decompression method that seems to be a little more reliable but a lot slower.
- Extract the zip file before running install.bat.
- make sure to use a high quality cable. The default apple one should be fine.
- the first time running the script might prompt a driver installation (WeTest USB or sth). Currently the only way to get it to work is to install it.
- if windows firewall interferes, allow everything.
- anti-virus software is known to cause issues with this. Consider deactivating it.
- if you're editing shortcut.bat with the default windows editor, it might happen that Defender thinks a temporary file created by the editor itself is dangerous. Idk why, as a workaround I'd recommend to use something like notepad++
- Install a copy of iTunes directly from Apple, not the MS Store
- make sure your device is unlocked
- Connect your PC to the internet, that's required to mount the PersonalizedDeveloperDiskImage
- Some PC devices have software/bios settings that automatically disable wifi if a wired connection is detected. Disable that software if you're running into issues where your wifi turns off.
- If the script says done but you don't have JIT enabled it's likely you didn't use a supported install method. For JIT to work you do need an app sideloaded using a dev cert, this is a limitation by Apple.
- Currently, there are a few reports with the script saying "Device not connected" even though it is. Usually this is driver related. Here is all the information I got on how to fix that: https://github.com/fritzlb/iOS17-JIT-WIN/issues/8#issuecomment-2024064032
- China's 'Great Firewall' is known to cause problems during install. The script downloads a bunch of dependencies and apparently someone doesn't like that. There's nothing I can do about that, sorry.
- Some languages using characters not in the english alphabet may cause issues. This is currently being investigated, see here for more information (and for a potential fix for korean systems): https://github.com/fritzlb/iOS17-JIT-WIN/pull/40

# Tips
- Because many people had issues with this: the release version of Pojavlauncher for iOS doesn't support MC 1.20. Use a lower MC version or try out a developer build of Pojavlauncher. For me, the ios build (NOT the slimmed version!) from this website worked: https://github.com/PojavLauncherTeam/PojavLauncher_iOS/actions/runs/7498475877
- If you're on an iPhone 15 pro, use the beta release of dolphiniOS if your app crashes.
- if you have an issue, please provide the full terminal output, this makes helping a lot easier and also more fun. I'll close any bug reports without this.

# License
Because of the integration of pymobiledevice3 I pretty much have no choice but to license this under GPLv3.

# Credits
This script relies heavily on pymobiledevice3 for iOS device communication. Thank you especially to doronz88!  
Check out the pymobildevice3 GitHub Repository here: https://github.com/doronz88/pymobiledevice3  
  
For attaching a debugger, this script uses llvm-mingw. Thank you to everyone involved there!  
Github: https://github.com/mstorsjo/llvm-mingw

    
This project is not associated with anyone, especially not with Apple, pymobiledevice3 or llvm-mingw. 
