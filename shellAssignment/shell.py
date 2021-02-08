#Joseph Medina - Sandoval

import os

#from aa-chatbot.py modified
class ConsoleReader:
    def __init__(self):
        pass

    def get_next_line(self):
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
        print('line:', line)
        if line[0] == '#':
            line = self.file_lines.pop(0)

        return line.split(" ")

class TaskExecuter:
    def __init__(self):
        pass

    def execute_task(self,args):
        child_pid = self.execute_background_task(args)
        os.waitpid(child_pid,0)

    def execute_background_task(self,argsList):
        child_process = os.fork()
        if child_process == 0:
            try:
                os.execv('/usr/bin/' + argsList[0],argsList)
            except FileNotFoundError:
                os._exit(0)
        return child_process

class Shell:
    def __init__(self,reader):
        self.argsList = []
        self.running = False
        self.reader = reader
        self.executioner = TaskExecuter()

    def start_run(self):
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.argsList = self.reader.get_next_line()
            if len(self.argsList) == 1 and self.argsList[0] == 'exit':
                self.exit_run()
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

        # if self.argsList[0] == 'echo' and self.argsList[-1] == '$?':
        #     pid = os.fork()
        #     if pid == 0:
        #         os.execv('/usr/bin/' +self.argsList[0], self.argsList)

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
        #for knowing when to run background tasks
        if self.argsList[-1][-1] == '&':
            self.executioner.execute_background_task(self.argsList)
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
