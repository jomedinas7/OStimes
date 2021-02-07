import sys
import traceback

class Bot:
    def __init__(self, reader):
        self.answer = ""
        self.reader = reader

    def start_conversation(self):
        self.ask_for_gender()
        self.ask_for_major()
        self.ask_for_favorite_animals()
        self.send_animal_response()
    
    def ask_for_gender(self):
        print("Hello, are you male or female?")
        self.answer = self.reader.get_next_line()

    def ask_for_major(self):
        if self.answer == "female":
            print("How excellent! are a CS major?")
        elif self.answer == "male":
            print("Me too. Are you a CS major?")
        else:
            print("really good! Are you a CS major?")

        self.answer = self.reader.get_next_line()

    def ask_for_favorite_animals(self):
        if self.answer == "no":
            print("too bad. Anyway, what's an animal you like, and two you don't?")
        if self.answer == "yes":
            print("Excellent, I am too. What's an animal you don't like, and two you do?")
        else:
            print("Ok then, what's an animal you like and two you don't?")

        self.answer = self.reader.get_next_line()

    def send_animal_response(self):
        answer_list = self.answer.split(" ")
        print(answer_list[0], "awesome, but I hate", answer_list[-1])


class ConsoleReader:
    def __init__(self):
        pass
    
    def get_next_line(self):
        return input()

class FileReader:
    def __init__(self, filename):
        with open(filename) as f:
            content = f.readlines()
        self.file_lines = [x.strip() for x in content] 

    def get_next_line(self):
        return self.file_lines.pop(0)

def main():
    try:
        start_bot()
    except FileNotFoundError:
        print("File was not found")
    except IndexError:
        print("File has not enought lines to conversate")
    except BaseException:
        print("No valid arguments")

def start_bot():
    reader = get_reader()
    bot = Bot(reader)
    bot.start_conversation()

def get_reader():
    if len(sys.argv) == 1:
        return ConsoleReader()
    
    if len(sys.argv) == 2:
        return FileReader(sys.argv[1])
    
    raise BaseException
    

main()