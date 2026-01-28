import re
from enum import Enum

class Token(Enum):
    ID     = "ID"           #added the required tokens
    NUM    = "NUM"
    IGNORE = "IGNORE"
    HNUM = "HNUM"
    INCR = "INCR"
    PLUS = "PLUS"
    MULT = "MULT"
    SEMI = "SEMI"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    ASSIGN = "ASSIGN"
                        
    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    INT = "INT"
    FLOAT = "FLOAT"
    IGNORE + "IGNORE"




class Lexeme:
    def __init__(self, token:Token, value:str) -> None:
        self.token = token
        self.value = value

    def __str__(self):
        return "(" + str(self.token) + "," + "\"" + self.value + "\"" + ")"    

def idy(l:Lexeme) -> Lexeme:
        return l

keywords ={                     #matched the keywords with their tokens
        "if": Token.IF,
        "else": Token.ELSE,
        "while": Token.WHILE, 
        "int": Token.INT,
        "float": Token.FLOAT,
        }

def check(l: Lexeme) -> Lexeme:
        keyword = keywords.get(l.value)
        if keyword is not None:
            return Lexeme(keyword, l.value)
        return l


tokens = [                                      #regular expressions for each tokens using the re library 
        (Token.IGNORE, r"[ \t\r\n]+", idy),
        (Token.INCR, r"\+\+", idy),
        (Token.PLUS, r"\+", idy),
        (Token.MULT, r"\*", idy),
        (Token.ASSIGN, r"=", idy),
        (Token.SEMI, r";", idy),
        (Token.LPAREN, r"\(", idy),
        (Token.RPAREN, r"\)", idy),
        (Token.LBRACE, r"\{", idy),
        (Token.RBRACE, r"\}", idy),
        (Token.HNUM, r"0[xX][0-9a-fA-F]+", idy),
        (Token.ID,     r"[A-Za-z][A-Za-z0-9]*",  check),
        (Token.NUM,    r"(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)",  idy),
]
