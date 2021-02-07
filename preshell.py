import os

def add_to_run(procList, args):
    procList.append(os.fork())
    if procList[-1] == 0:
        os.execv('/usr/bin/'+args[0],args)

def wait_for_all(processes):
    for procID in processes:
        os.waitpid(procID,0)

def main():
    proc = []
    add_to_run(proc,['cat', '/proc/cpuinfo'])
    add_to_run(proc,['echo', 'Hello World'])
    add_to_run(proc,['python3', 'spinner.py', '1000000'])
    add_to_run(proc,['uname', '-a'])

    wait_for_all(proc)
    add_to_run(proc, ['python3', 'spinner.py', '2000000'])

main()
