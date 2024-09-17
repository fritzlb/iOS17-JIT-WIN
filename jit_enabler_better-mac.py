#!/usr/bin/env python3
import subprocess
import time
import sys
import atexit
import pymobiledevice3


def exit_func(tunnel_proc):
    tunnel_proc.terminate()

def print_error(errorcode, description):
    print(f"{errorcode}: {description}")
        


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
        print_error("invalid bundle ID", f"usage: {sys.argv[0]} [bundle_id]")
        sys.exit()
    try:
        debug = args[2]
        if debug:
            print("DEBUG mode specified.")
    except:
        pass
    print(f"Got bundle ID: {bundle_id}")
    print("Starting tunnel to device...")
    print("This might take a while. If it freezes, close this window and kill every python process in Activity Monitor or reboot your Mac.")

    # Run pymobiledevice3 as subprocess, exit and log errors if tunnel crashes
    tunnel_process = subprocess.Popen(["python3", "-m", "pymobiledevice3", "remote", "start-tunnel", "--script-mode"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
                    if b'connected' in error[i]:
                        not_connected = True
                    if b'admin' in error[i]:
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
    print(f"Successfully created tunnel: {rsd_str}")

    # Mount disk image
    print("Manually trying to mount DeveloperDiskImage...")
    dev_img_proc = subprocess.Popen(["python3", "-m", "pymobiledevice3", "mounter", "auto-mount"], stderr=subprocess.PIPE)
    ret_val = dev_img_proc.communicate()[1].decode()

    if debug:
        print(ret_val)

    if "success" in ret_val:
        print("Mounted Disk image.")
    elif "already" in ret_val:
        print("Diskimage already mounted.")
    else:
        print("Mounting DiskImage failed. Trying the alternative method...")
        dev_img_proc_alt = subprocess.Popen(["python3", "-m", "pymobiledevice3", "mounter", "auto-mount", "--rsd", rsd_str], stderr=subprocess.PIPE)
        ret_val2 = dev_img_proc_alt.communicate()[1].decode()

        if debug:
            print(ret_val2)

        if "success" in ret_val2:
            print("Successfully mounted using alternative method.")
        elif "already" in ret_val2:
            print("Image already mounted.")
        else:
            print_error("Error mounting DiskImage", ret_val)
            print_error("Error using alternative method", ret_val2)
            sys.exit()

    # Launch app
    rsd_address, rsd_port = rsd_str.split(" ")
    cmd = ["python3", "-m", "pymobiledevice3", "developer", "dvt", "launch", bundle_id, "--rsd", rsd_address, rsd_port]
    print(f"RSD Address: {rsd_address}")
    print(f"RSD Port: {rsd_port}")
    #cmd = ["python3", "-m", "pymobiledevice3", "developer", "dvt", "launch", bundle_id, "--rsd", rsd_str]
    print("Starting app...")
    launch_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret_val = launch_proc.communicate()

    if debug:
        print(ret_val)

    try:
        if_cond = ret_val[1].decode().strip()
    except:
        print_error("Unknown error.", ret_val)
        sys.exit()

    if if_cond:
        print_error("Error launching the app. Did you specify the correct bundle ID?", ret_val[1].decode())
        sys.exit()

    pid = ret_val[0].decode().replace("Process launched with pid ", "").strip()
    print(f"Started app. PID: {pid}")

    # Start debug server
    print("Starting debug server...")
    cmd = ["python3", "-m", "pymobiledevice3", "developer", "debugserver", "start-server", "--rsd", rsd_str]
    debug_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ret_val = debug_proc.communicate()

    if debug:
        print(ret_val)

    debug_info = ret_val[0].decode().replace(
        "\r\nFollow the following connections steps from LLDB:\r\n\r\n(lldb) platform select remote-ios\r\n(lldb) target create /path/to/local/application.app\r\n"
        "(lldb) script lldb.target.module[0].SetPlatformFileSpec(lldb.SBFileSpec('/private/var/containers/Bundle/Application/<APP-UUID>/application.app'))\r\n"
        "(lldb) process connect connect://", "").replace("   <-- ACTUAL CONNECTION DETAILS!\r\n(lldb) process launch\r\n\r\n", "")

    if ret_val[1].decode():
        print_error("Debug server error", ret_val[1].decode())
        sys.exit()

    print(f"Started debug server with connection details: {debug_info}")

    # Attach and detach LLDB
    print("Run debugging commands...")
    print("This might take a few minutes.")
    debug_address = debug_info
    cmdfile_path = "cmdfile.txt"

    try:
        cmdfile = open(cmdfile_path, "w")
    except:
        cmdfile = open(cmdfile_path, "x")

    cmdfile.write(f"gdb-remote {debug_address}\nsettings set target.memory-module-load-level minimal\nattach -p {pid}\ndetach\n quit")
    cmdfile.close()

    # Modify LLDB command for macOS
    cmd_lldb = ['lldb']

    lldb_process = subprocess.Popen(cmd_lldb, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True)
    input_data = f"command source -s 0 {cmdfile_path}"

    stdout, stderr = lldb_process.communicate(input=input_data)

    if debug:
        print(stdout, stderr)

    print("Done.")
    if debug:
        print("DEBUG mode specified. This script won't quit automatically. Press CTRL + C to stop it.")
        while True:
            pass
