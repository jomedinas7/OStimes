#Joseph Medina - Sandoval

import os
import sys
#from aa-chatbot.py modified
class ConsoleReader:
    def __init__(self):
        pass

    def get_next_line(self):
        #getting the value of the PS1 environment variable
        if os.getenv("PS1") == None:
            return input('$$$$ ').split(" ")
        return input(os.getenv("PS1")).split(" ")

#from aa-chabot.py modified slightly
class FileReader:
    def __init__(self, filename):
        with open(filename) as f:
            content = f.readlines()
        self.file_lines = [x.strip() for x in content]

    def get_next_line(self):
        line = self.file_lines.pop(0)
        if line[0] == '#':
            #skip the line
            line = self.file_lines.pop(0)

        return line.split(" ")

class TaskExecuter:
    def __init__(self):
        self.redirectedInput = False
        self.redirectedOutput = False

        #inspired by Dr. Freudenthal's exec demo
    def execute_task(self,argsList):
        child_process = os.fork()
        if child_process <0:
            sys.exit(1)
        elif child_process == 0:
            if self.redirectedOutput:
                print('WOOP')
                self.redirect_output(argsList[-1])
                new_args = argsList
                for i in range(len(new_args)):
                    if new_args[i] == '>':
                        argsList = new_args[:i]
            #search in directories and attempt to run commands
            for path in os.environ['PATH'].split(os.pathsep):
                try:
                    os.execv(path +'/' + argsList[0],argsList)
                except FileNotFoundError:
                    pass #fail silently
            sys.exit(1)
        else: #child_process >0
            if argsList[-1] != "&": # indicate background task
                exit_code = os.waitpid(child_process,0) #will assign list containing exit code
                if exit_code[1] != 0:
                    print("Program terminated: exit code ", exit_code[1])

    def redirect_output(self, dest):
        os.close(1) # Redirect child's stdout
        os.open(dest, os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)

    def redirect_input(self, src):
        os.close(0) # Redirect child's stdin
        os.open(src, os.O_CREAT | os.O_RDONLY)
        os.set_inheritable(0, True)
    # def redirect_output(self,src_args,dest):
    #     child_id = os.fork()
    #     if child_id == 0:
    #         try:
    #             fd = os.open(dest, os.O_WRONLY | os.O_CREAT)
    #             os.dup2(fd, 1)
    #             os.execv('/usr/bin/' + src_args[0], src_args)
    #         except FileNotFoundError:
    #             print('That is not a valid command')
    #             os._exit(0)



class Shell:
    def __init__(self,reader):
        self.argsList = []
        self.running = False
        self.reader = reader
        self.executioner = TaskExecuter() #it sounded cooler in my head

    def start_run(self):
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.argsList = self.reader.get_next_line()
            if len(self.argsList) == 1 and self.argsList[0] == 'exit':
                self.exit_run()
            else:
                self.process_input()
        return

    def exit_run(self):
        print('Exit successful.')
        self.running = False
        return


    def process_input(self):
        #handle empty args list
        if len(self.argsList) == 1 and self.argsList[0] == '':
            print('Invalid input')
            return

        #special cd input
        if self.argsList[0] == 'cd':
            print('cd found')
            os.chdir(self.argsList[1])
            return
        #special flag to catch PS1 change
        if self.argsList[0][0:3] == 'PS1':
            lolita = self.argsList[0].split("=")
            os.environ['PS1']  = lolita[1]
            return
        #redirecting output
        if '>' in self.argsList:
            # args = ' '.join(self.argsList)
            # redirection = args.split('>')
            # command_args = redirection[0].split()
            # dest = redirection[1].replace(' ', '')
            # self.executioner.redirect_output(command_args, dest)
            # return
            self.executioner.redirectedOutput = True
            self.executioner.execute_task(self.argsList)
            return
        else:
            self.executioner.execute_task(self.argsList)


def main():
    choice = input('1. File \n2. Input\n>>')
    if choice == '1':
        myReader = FileReader('test.txt')
    elif choice == '2':
        myReader = ConsoleReader()
    myShell = Shell(myReader)
    myShell.start_run()

main()
