import os
import sys
import re


class Shell:
    def __init__(self, reader):
        self.answer = ""
        self.reader = reader
        self.prompt_symbol = "$$$$"

    def run_shell(self):
        self.set_prompt_symbol()

        while self.answer != "exit":
            if len(sys.argv) == 1: # Only print prompt symbol if getting user input
                print(self.prompt_symbol, end=" ")
            self.answer = self.reader.read_line()
            self.run_command(self.answer)
        sys.exit(0)


    def run_command(self, answer):
        if (len(answer) == 0) or (answer == "exit") or (answer[0] == "#"):
            return

        args = answer.split(" ")
        if args[0] == "cd": # Want to change directory
            self.change_dir(args)
            return

        if ">" in args: # Redirecting output of source into destination
            self.execute_command(args, redirect_output=True)
            return

        if "<" in args: # Redirecting input of source into destination
            self.execute_command(args, redirect_input=True)
            return

        if "|" in args: # Using pipe to let processes communicate
            src, dest = [], []
            for i in range(len(args)):
                if args[i] == "|":  # Will separate left and right args
                    src = args[:i]
                    dest = args[i+1:]
            for i in range(len(src)): # Remove empty entries
                if src[i] == "":
                    src.pop(i)
            self.use_pipe(args,src,dest)
            return

        self.execute_command(args) # Regular command


    def set_prompt_symbol(self):
        if os.environ.get('PS1') is not None:
            self.prompt_symbol = os.environ.get('PS1')


    def change_dir(self, args):
        try:
            if len(args) > 1:
                path = args[1]
                os.chdir(path)
        except Exception:
            print("Invalid path!")


    def get_source_command(self, args):
        for i in range(len(args)): # Gets params for command to work as src
            if args[i] == ">" or args[i] == "<" or args[i] == "|":
                return args[:i]
        return args

    def redirect_output(self, dest):
        os.close(1) # Redirect child's stdout
        os.open(dest, os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1, True)

    def redirect_input(self, src):
        os.close(0) # Redirect child's stdin
        os.open(src, os.O_CREAT | os.O_RDONLY)
        os.set_inheritable(0, True)

    def find_path(self, args):
        path = os.environ['PATH']
        for dir in path.split(":"): # Look for command in all directories in path
            possiblePath = "%s/%s" % (dir, args[0])
            if os.path.isfile(possiblePath):
                return possiblePath
        possiblePath = "%s/%s" % (os.getcwd(), args[0])

        if os.path.isfile(possiblePath): # If command is in current working directory
            return possiblePath

        return None


    def use_pipe(self, args, src, dest):
        pr, pw = os.pipe() # File descriptors for reading and writing
        children = []
        for f in (pr, pw):
            os.set_inheritable(f, True)
        child1 = os.fork()
        children.append(child1)
        if child1 == 0:
            os.close(1) # Redirect child's stdout
            os.dup2(pw,1)
            for fd in (pr, pw): # Close fd's
                os.close(fd)
            path = self.find_path(src)
            if path is not None:
                os.execv(path, src)

        child2 = os.fork()
        children.append(child2)
        if child2 == 0:
            os.close(0) # Redirect child's stdin
            os.dup2(pr,0)
            for fd in (pw, pr): # Close fd's
                os.close(fd)
            path = self.find_path(dest)
            if path is not None:
                os.execv(path, dest)

        for fd in (pw, pr): # Close fd's
            os.close(fd)

        for c in children: # Wait for children
            ec = os.waitpid(c, 0)
            if ec[1] != 0:
                print("Program terminated: exit code ", ec[1])


    def execute_command(self, args, redirect_output=False, redirect_input=False):
        path = self.find_path(args)

        if args[0] == "chmod": # Adds directory of executable to be made to 'PATH' to later access it
            os.environ['PATH'] = os.environ['PATH'] + ":" +  os.getcwd()

        if path is not None: # Valid command found
            rc = os.fork()
            if rc == 0:
                if redirect_output: # Input has >
                    self.redirect_output(args[-1])
                if redirect_input: # Input has <
                    self.redirect_input(args[-1])

                args = self.get_source_command(args)
                os.execv(path, args)
            else:
                if args[-1] != "&": # We will wait for child to finish
                    ec = os.waitpid(rc,0)
                    if ec[1] != 0:
                        print("Program terminated: exit code ", ec[1])
        else:
            print("Command: %s not found" % (args[0]))


class ConsoleReader:
    def __init__(self):
        pass
    def read_line(self):
        return input()


class FileReader:
    def __init__(self, file):
        with open(file) as f:
            content = f.readlines()
        self.lines = [x.strip() for x in content]

    def read_line(self):
        return self.lines.pop(0)


def select_reader():
    if len(sys.argv) == 1:
        return ConsoleReader()
    if len(sys.argv) == 2:
        return FileReader(sys.argv[1])
    raise Exception


def main():
    try:
        reader = select_reader()
    except Exception:
        print("Invalid arguments!")

    shell = Shell(reader)
    shell.run_shell()


if __name__ == "__main__":
    main()
