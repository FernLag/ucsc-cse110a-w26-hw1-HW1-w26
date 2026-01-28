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

class NGScanner:
    def __init__(self, tokens: List[Tuple[Token,str,Callable[[Lexeme],Lexeme]]]) -> None:
        self.tokens = tokens

    def input_string(self, input_string:str) -> None:
        self.istring = input_string
        
    def token(self) -> Optional[Lexeme]:
        # Implement me!

        if not hasattr(self, "istring") or len(self.istring) == 0:  #basic check similar to previous part
            return None

        if not hasattr(self, "master_re"):
            group = []
            self.ng_names = []          #these help to map from the groups to the tokens, have a main named group
            self.ng_tokens = []
            self.ng_action = []
            for (tok, pattern, action) in self.tokens:
                name = tok.value
                self.ng_names.append(name)
                self.ng_tokens.append(tok)
                self.ng_action.append(action)

                group.append("(?P<" + name + ">" + pattern + ")")       
            self.master_re = re.compile("|".join(group))            #compile the main group

        m = self.master_re.match(self.istring)      #match one token at start
        if m is None:
            raise ScannerException()

        name = m.lastgroup      #see which tetx had matched 
        text = m.group(0) 

        self.istring = self.istring[len(text):]
        i = self.ng_names.index(name)
        lex = Lexeme(self.ng_tokens[i], text)
        lex = self.ng_action[i](lex)
        if lex.token == Token.IGNORE:
            return self.token()

        return lex

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

    s = NGScanner(tokens)
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
