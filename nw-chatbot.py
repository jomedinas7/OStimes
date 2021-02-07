#!/usr/bin/python3
# sampleChatbot.py
# Nigel Ward, UTEP, January 2021

import sys

responseDict = {
   'yes': 'Excellent, I am too.  What\'s an animal you don\'t like, and two you do?',
   'no': 'Too bad.  Anyway, what\'s an animal you like, and two you don\'t?',
   'female': 'How excellent! Are you a CS major?',
   'male': 'Me too.  Are you a CS major?'
}

def lookupResponse(line):
   words = line.split()
   firstWord =  words[0].rstrip()
   if firstWord in responseDict.keys():
      return responseDict[firstWord]
   else:
      print(firstWord + ": awesome, but I hate " + words[-1] + " too. Bye for now.")
      exit(0)


readingFromFile = False 
if len(sys.argv) > 1:
   fd = open(sys.argv[1], "r")
   readingFromFile = True
else:
   fd = sys.stdin
   print("Hello, are you male or female?")
with fd as openfileobject:
   for line in openfileobject:
      if readingFromFile:
         print("user says: " + line.rstrip())
         print(lookupResponse(line.rstrip()))
            

              
