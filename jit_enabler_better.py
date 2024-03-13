import subprocess
import time
import sys
import atexit
import pymobiledevice3


def exit_func(tunnel_proc):
    tunnel_proc.terminate()

def print_error(errorcode, description):
    print(errorcode, ":", description)
        


if __name__ == "__main__":
    debug = False
    #read arguments
    print("Getting bundle ID...")
    args = sys.argv
    try:
        bundle_id = sys.argv[1]
    except:
        bundle_id = ""
    if bundle_id == "":
        print_error("invalid bundle ID", "usage: " + sys.argv[0] + " [bundle_id]")
        sys.exit()
    try:
        debug = args[2]
        if debug:
            print("DEBUG mode specified.")
    except:
        pass
    print("Got bundle ID:", bundle_id)
    print("starting tunnel to device...")
    print("This might take a while. In case it freezes, either close this window and kill every python process in task manager or simply reboot your PC.")
    #run pymobiledevice3 as subprocess, exit and log errors if tunnel crashes
    tunnel_process = subprocess.Popen("python -m pymobiledevice3 remote start-tunnel --script-mode", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    atexit.register(exit_func, tunnel_process)
    while True:
        output = tunnel_process.stdout.readline()
        if output:
            rsd_val = output.decode().strip()
            break
        if tunnel_process.poll() is not None:
            error = tunnel_process.stderr.readlines()
            if error:
                not_connected = None
                admin_error = None
                for i in range(len(error)):
                    if (error[i].find(b'connected') > -1):
                        not_connected = True
                    if (error[i].find(b'admin') > -1):
                        admin_error = True
                if not_connected:
                    print_error("It seems like your device isn't connected.", error)
                elif admin_error:
                    print_error("It seems like you're not running this script as admin, which is required.", error)
                else:
                    print_error("Error opening a tunnel.", error)
                sys.exit()
            break
    rsd_str = str(rsd_val)
    print("Sucessfully created tunnel: " + rsd_str)

    #mount diskimage

    print("Manually trying to mount DeveloperDiskImage (this seems to prevent errors on some systems)...")
    dev_img_proc = subprocess.Popen("python -m pymobiledevice3 mounter auto-mount", stderr = subprocess.PIPE)
    ret_val = dev_img_proc.communicate()[1].decode()
    if debug:
        print(ret_val)
    if ret_val.find("success") > -1:
        print("Mounted Disk image.")
    elif ret_val.find("already") > -1:
        print("Diskimage already mounted.")
    else:
        print_error("Error mounting DiskImage", ret_val)
        sys.exit()
    

    #launch proc
    cmd = "python -m pymobiledevice3 developer dvt launch " + bundle_id + " --rsd " + rsd_str
    print("Starting app...")
    launch_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret_val = launch_proc.communicate()
    if debug:
        print(ret_val)
    try:
        if_cond = ret_val[1].decode().replace("\r\n", "")
    except:
        print_error("Unknown error.", ret_val)
        sys.exit()
    if if_cond != "": #display error in case starting app fails
        print_error("Error launching the app. Did you specify the correct bundle ID?", ret_val[1].decode())
        sys.exit()
    pid = ret_val[0].decode().replace("Process launched with pid ", "").replace("\r\n", "")
    print("Started app. PID: " + pid)

    # debug server

    print("Starting debug server...")
    cmd = "python -m pymobiledevice3 developer debugserver start-server" + " --rsd " + rsd_str
    debug_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    ret_val = debug_proc.communicate()
    if debug:
        print(ret_val)
    debug_info = ret_val[0].decode().replace("\r\nFollow the following connections steps from LLDB:\r\n\r\n(lldb) platform select remote-ios\r\n(lldb) target create /path/to/local/application.app\r\n(lldb) script lldb.target.module[0].SetPlatformFileSpec(lldb.SBFileSpec('/private/var/containers/Bundle/Application/<APP-UUID>/application.app'))\r\n(lldb) process connect connect://", "").replace("   <-- ACTUAL CONNECTION DETAILS!\r\n(lldb) process launch\r\n\r\n","")
    if ret_val[1].decode() != "":
        print_error("debug server error", ret_val[1].decode())
        sys.exit()
    print("Started debug server with connection details: " + debug_info)

    #attach and deattach lldb
    print("Run debugging commands...")
    print("This might take a few minutes.")
    debug_adress = debug_info
    cmdfile_path = "cmdfile.txt"
    try:
        cmdfile = open(cmdfile_path, "w")
    except:
        cmdfile = open(cmdfile_path, "x")
    cmdfile.write("gdb-remote " + debug_adress + "\nsettings set target.memory-module-load-level minimal\nattach -p " + pid + "\ndetach\n quit")
    cmdfile.close()


    cmd_lldb = ['llvm-mingw-20231128-msvcrt-x86_64/bin/lldb.exe']

    lldb_process = subprocess.Popen(cmd_lldb, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
    input_data = "command source -s 0 " + cmdfile_path

    stdout, stderr = lldb_process.communicate(input=input_data)
    if debug:
        print(stdout, stderr)
    print("done.")
    if debug:
        print("DEBUG mode specified. This script won't quit automatically. Press CTRL + C to stop it.")
        while True:
            pass
