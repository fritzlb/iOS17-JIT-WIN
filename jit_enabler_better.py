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
    print("Getting bundle ID...")
    args = sys.argv
    try:
        bundle_id = sys.argv[1]
    except:
        bundle_id = ""
    if bundle_id == "":
        print_error("invalid bundle ID", "usage: " + sys.argv[0] + " [bundle_id]")
        sys.exit()
    print("Got bundle ID:", bundle_id)
    print("starting tunnel to device...")
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
                print_error("Error opening a tunnel.", error)
                sys.exit()
            break
    rsd_str = str(rsd_val)
    print("Sucessfully created tunnel: " + rsd_str)

    #launch proc
    cmd = "python -m pymobiledevice3 developer dvt launch " + bundle_id + " --rsd " + rsd_str
    print("Starting app...")
    launch_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    pid = launch_proc.communicate()[0].decode().replace("Process launched with pid ", "").replace("\r\n", "")
    print("Started app. PID: " + pid)

    print("Starting debug server...")
    cmd = "python -m pymobiledevice3 developer debugserver start-server" + " --rsd " + rsd_str
    debug_proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    debug_info = debug_proc.communicate()[0].decode().replace("\r\nFollow the following connections steps from LLDB:\r\n\r\n(lldb) platform select remote-ios\r\n(lldb) target create /path/to/local/application.app\r\n(lldb) script lldb.target.module[0].SetPlatformFileSpec(lldb.SBFileSpec('/private/var/containers/Bundle/Application/<APP-UUID>/application.app'))\r\n(lldb) process connect connect://", "").replace("   <-- ACTUAL CONNECTION DETAILS!\r\n(lldb) process launch\r\n\r\n","")
    print("Started debug server with connection details: " + debug_info)

    #attach and deattach lldb
    print("Run debugging commands...")
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
    print("done.")
