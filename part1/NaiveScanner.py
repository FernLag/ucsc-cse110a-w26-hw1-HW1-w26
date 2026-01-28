import string
import argparse
from time import time
from enum import Enum
from typing import Optional

class ScannerException(Exception):
    pass

class StringStream:
    def __init__(self, input_string: str) -> None:
        self.string = input_string

    def is_empty(self) -> bool:
        return len(self.string) == 0

    def peek_char(self) -> Optional[str]:
        if not self.is_empty():            
            return self.string[0]
        return None

    def eat_char(self) -> None:
        # take the first character off the string
        self.string = self.string[1:]

# put characters to ignore in this array        
IGNORE = [" ", "\n", "\t", "\r"]
NUMS   = [str(x) for x in range(10)]

# From: https://www.adamsmith.haus/python/answers/how-to-make-a-list-of-the-alphabet-in-python
alphabet_string = string.ascii_lowercase
CHARS = list(alphabet_string)

class Token(Enum):
    ADD    = "ADD"
    MULT   = "MULT"     #added the INCR and SEMI tokens
    ASSIGN = "ASSIGN"
    SEMI   = "SEMI"
    ID     = "ID"
    NUM    = "NUM"
    INCR = "INCR"

class Lexeme:
    def __init__(self, token:Token, value:str) -> None:
        self.token = token
        self.value = value

    def __str__(self):
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"

class NaiveScanner:

    def __init__(self, input_string:str) -> None:
        self.ss = StringStream(input_string)
        self.line = 1
    def token(self) -> Optional[Lexeme]:

        # First handle the ignore case
        while self.ss.peek_char() in IGNORE:
            if self.ss.peek_char() == "\n":
                self.line += 1
            self.ss.eat_char()

        # If there is nothing to return, return None
        if self.ss.is_empty():
            return None

        # Scan for the single character tokens
        if self.ss.peek_char() == "+":
            if len(self.ss.string) >= 2 and self.ss.string[1] == "+":       #used for the case of when there are two + in a row so they won't each be considered as an add
                self.ss.eat_char()
                self.ss.eat_char()
                return Lexeme(Token.INCR, "++")
            else:
                self.ss.eat_char()
                return Lexeme(Token.ADD, "+")
        
        if self.ss.peek_char() == "*":
            self.ss.eat_char()
            return Lexeme(Token.MULT, "*")

        if self.ss.peek_char() == "=":
            self.ss.eat_char()
            return Lexeme(Token.ASSIGN, "=")

        if self.ss.peek_char() == ";":          #also put them here 
            self.ss.eat_char()
            return Lexeme(Token.SEMI, ";")

        if self.ss.peek_char() == "++":
            self.ss.eat_char()
            return Lexeme(Token.INCR, "++")

    

        if self.ss.peek_char() in CHARS:        #for ID requirement, it consumes the leading digits 
            value = ""
            while True:
                c = self.ss.peek_char()
                if c in CHARS or c in NUMS:
                    value += c
                    self.ss.eat_char()
                else:
                    break
            return Lexeme(Token.ID, value)


        if self.ss.peek_char() in NUMS:             #checks if there is a decimal and if so there has to be  a digit after
            value = ""
            while self.ss.peek_char() in NUMS:
                value += self.ss.peek_char()
                self.ss.eat_char()
            if self.ss.peek_char() == ".":
                value += "."
                self.ss.eat_char()

                if self.ss.peek_char() not in NUMS:
                    raise ScannerException()

                while self.ss.peek_char() in NUMS: 
                    value += self.ss.peek_char()
                    self.ss.eat_char()

                if self.ss.peek_char() == ".":
                    raise ScannerException()
            return Lexeme(Token.NUM, value)
        raise ScannerException(f"Error on line {self.line}")




        # Scan for the multi character tokens
       # if self.ss.peek_char() in CHARS:
        #    value = ""
         #   while self.ss.peek_char() in CHARS:
          #      value += self.ss.peek_char()
           #     self.ss.eat_char()
           # return Lexeme(Token.ID, value)

        #if self.ss.peek_char() in NUMS:
         #   value = ""
          #  while self.ss.peek_char() in NUMS:
           #     value += self.ss.peek_char()
            #    self.ss.eat_char()
            #return Lexeme(Token.NUM, value)

        # if we cannot match a token, throw an exception
        # you should implement a line number to pass
        # to the exeception
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    
    f = open(args.file_name)    
    f_contents = f.read()
    f.close()

    verbose = args.verbose

    s = NaiveScanner(f_contents)

    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if (verbose):
            print(t)
    end = time()
    print("time to parse (seconds): ",str(end-start))
