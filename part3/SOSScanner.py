import re
from functools import reduce
from time import time
import argparse
import pdb
import sys
sys.path.append("../part2/")
from tokens import tokens,Token,Lexeme
from typing import Callable,List,Tuple,Optional


# No line number this time
class ScannerException(Exception):
    pass

class SOSScanner:
    def __init__(self, tokens: List[Tuple[Token,str,Callable[[Lexeme],Lexeme]]]) -> None:
        self.tokens = tokens

    def input_string(self, input_string:str) -> None:
        self.istring = input_string

    def token(self) -> Optional[Lexeme]:
        # Implement me!

        if len(self.istring) == 0:      #basic check to see if length is 0
            return None

        for (tok, pattern, action) in self.tokens:
            m = re.match(pattern, self.istring)     #match the start of each string 
            if m is None: 
                continue        #if token doesn't match then continue 
            text = m.group(0)   #prefix match with token 

            self.istring = self.istring[len(text):]

            lex = Lexeme(tok, text) #create a Lexeme for the match and then apply the action
            lex = action(lex)

            if lex.token == Token.IGNORE:
                return self.token()

            return lex
        raise ScannerException()

        #pass

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('file_name', type=str)
    parser.add_argument('--verbose', '-v', action='store_true')
    args = parser.parse_args()
    
    f = open(args.file_name)    
    f_contents = f.read()
    f.close()

    verbose = args.verbose

    s = SOSScanner(tokens)
    s.input_string(f_contents)

    start = time()
    while True:
        t = s.token()
        if t is None:
            break
        if (verbose):
            print(t)
    end = time()
    print("time to parse (seconds): ",str(end-start))    
