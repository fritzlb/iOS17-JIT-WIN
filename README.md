# iOS17-JIT-WIN
Enable JIT on iOS 17 using a windows PC  
tested on windows 11 with an ipad on 17.3.1  
Video guide: https://youtu.be/MLHa2JLuk3Y 
# SETUP
Install python from https://www.python.org/downloads/. Make sure to add it to your PATH.  
Download/Clone this repo (green button -> download zip), extract the zip whereever you'd like and run install.bat by double clicking it.  
# Usage
Open an admin terminal by double clicking "open terminal here.bat".  
Run `python jit_enabler_better.py bundle_id` by typing it into the terminal window and finish the command by pressing enter.  
where bundle ID can be obtained e.g. inside AltStore under 'View App IDs'. If the correct one for your app doesn't show up, refresh your apps and try again.

# Issues
If you run into any problems or if anything in my instructions is unclear, feel free to open an issue with the FULL error message :)  
Here are some common troubleshooting tips though:  
- Reboot your PC. Use the restart button, shutting down and starting again isn't the same.
- make sure to use a high quality cable. The default apple one should be fine.
- the first time running the script might prompt a driver installation (WeTest USB or sth). Currently the only way to get it to work is to install it.
- if windows firewall interferes, allow everything.
- if you're editing shortcut.bat with the default windows editor, it might happen that Defender thinks a temporary file created by the editor itself is dangerous. Idk why, as a workaround I'd recommend to use something like notepad++
- Install a copy of iTunes directly from Apple, not the MS Store
- make sure your device is unlocked
- Connect your PC to the internet, that's required to mount the PersonalizedDeveloperDiskImage

# License
Feel free to do whatever you want with my code. Please note that everything installed by install.bat might be under other licenses. Also, there's absolutely no warranty or anything.
