# iOS17-JIT-WIN
Enable JIT on iOS 17 using a windows PC  
  
Video guide: https://youtu.be/MLHa2JLuk3Y  
  
Tested with Windows 11 and iOS 17.3.1 as well as 17.4.  
The following apps have been tested by me and do work:
- PojavLauncher (pay attention to the tips section down below!)
- UTM (AltStore release version)
- DolphiniOS (pay attention to the tips section down below!)

# SETUP
Install python from https://www.python.org/downloads/. Make sure to add it to your PATH.  
Download/Clone this repo (green button -> download zip), extract the zip whereever you'd like and run install.bat by double clicking it.  

# Usage
Open an admin terminal by double clicking "open terminal here.bat".  
Run `python jit_enabler_better.py {bundle_id}` by typing it into the terminal window and finish the command by pressing enter.  
Make sure to replace {bundle_ID} with your actual bundle ID, which can be obtained e.g. inside AltStore under 'View App IDs'. If the correct one for your app doesn't show up, refresh your apps and try again.

# Issues
If you run into any problems or if anything in my instructions is unclear, feel free to open an issue with the FULL error message :)  
Here are some common troubleshooting tips though:  
- Reboot your PC. Use the restart button, shutting down and starting again isn't the same.
- If there's an error like "Python was not found" follow the installation instructions and install python.
- If there's an error like "pymobiledevice3 not found", you probably forgot executing install.bat. Do that (again).
- If you get an error while running debug commands, try executing install_slow.bat. It'll redownload everything and use a decompression method that seems to be a little more reliable but a lot slower.
- Extract the zip file before running install.bat.
- make sure to use a high quality cable. The default apple one should be fine.
- the first time running the script might prompt a driver installation (WeTest USB or sth). Currently the only way to get it to work is to install it.
- if windows firewall interferes, allow everything.
- if you're editing shortcut.bat with the default windows editor, it might happen that Defender thinks a temporary file created by the editor itself is dangerous. Idk why, as a workaround I'd recommend to use something like notepad++
- Install a copy of iTunes directly from Apple, not the MS Store
- make sure your device is unlocked
- Connect your PC to the internet, that's required to mount the PersonalizedDeveloperDiskImage
- Some PC devices have software/bios settings that automatically disable wifi if a wired connection is detected. Disable that software if you're running into issues where your wifi turns off.

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
