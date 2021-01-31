import os

def wait_for_all(processes):
    for procID in processes:
        os.waitpid(procID,0)

def add_and_run(procList, args):
        procList = procList + [os.fork()]
        if procList[-1] == 0:
            os.execv('usr/bin/'+args[0],args,os.environ)

def main():
    proc = []
    add_and_run(proc,['cat', 'proc/cpuinfo'])
    add_and_run(proc,['echo', 'Hello World'])
    add_and_run(proc,['python3', 'spinner.py 1000000'])
    add_and_run(proc,['uname', '-a'])
