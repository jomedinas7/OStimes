#Joseph Medina - Sandoval

import os

#from aa-chatbot.py
class ConsoleReader:
    def __init__(self):
        pass

    def get_next_line(self):
        if os.getenv("PS1") == None:
            return input('$$$$ ').split(" ")
        return input(os.getenv("PS1")).split(" ")

#from aa-chabot.py
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

class Shell:
    def __init__(self,theReader):
        self.argsList = []
        self.running = False
        self.reader = theReader

    def start_run(self):
        self.running = True
        print('PS1: ',os.getenv("PS1"))
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

    def process_input(self):
        if len(self.argsList) == 1 and self.argsList[0] == '':
            print('Invalid input')
            return
        if self.argsList[0] == 'cd':
            print('cd found')
            os.chdir(self.argsList[1])
            return
        if self.argsList[0][0:3] == 'PS1':
            lolita = self.argsList[0].split("=")
            os.environ['PS1']  = lolita[1]
            return
        #most functions to be called this way are in /usr/bin/
        #streamline this input
        #try-catch block
        #class ProcessRunner?
        try:
            os.execv('/usr/bin/' + self.argsList[0], self.argsList)
        except FileNotFoundError:
            print("Invalid command")

        # if self.argsList[0] == 'ls':
        #     os.execv('/usr/bin/ls', self.argsList)
        # if self.argsList[0] == 'cat':
        #     os.execv('/usr/bin/cat', self.argsList)
        # if self.argsList[0] == 'grep':
        #     os.execv('/usr/bin/grep', self.argsList)
        # if self.argsList[0][0:3] == 'PS1':
        #     lolita = self.argsList[0].split("=")
        #     os.environ['PS1']  = lolita[1]



def main():
    choice = input('1. File \n2. Input\n>>')
    if choice == '1':
        myReader = FileReader('test.txt')
    elif choice == '2':
        myReader = ConsoleReader()
    myShell = Shell(myReader)
    myShell.start_run()

main()
