import os
import sys

class ConsoleReader:
    def __init__(self):
        pass

    def get_next_line(self):
        return input('>> ').split(" ")

class FileReader:
    def __init__(self, filename):
        with open(filename) as f:
            content = f.readlines()
        self.file_lines = [x.strip() for x in content]

    def get_next_line(self):
        line = self.file_lines.pop(0)
        if line[0] == '#':
            print('input:', line)
            return ''

        return line

class Shell:
    def __init__(self,theReader):
        self.argsList = []
        self.running = False
        self.reader = theReader

    def start_run(self):
        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.argsList = self.reader.get_next_line()
            if len(self.argsList) == 1 and self.argsList[0] == 'exit':
                print('Now exiting...')
                self.exit_run()
            self.process_input()

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
        if self.argsList[0] == 'ls':
            os.execv('/usr/bin/ls', self.argsList)
        if self.argsList[0] == 'cat':
            os.execv('/usr/bin/cat', self.argsList)
        if self.argsList[0] == 'grep':
            os.execv('/usr/bin/grep', self.argsList)
        return



def main():

    myReader = ConsoleReader()
    myShell = Shell(myReader)
    myShell.start_run()

main()
