# HW1-w26

## Part 1

### Correctness: Describe how your scanner extensions implement the required behavior, including any edge cases you handled.

I added the SEMI and INCR tokens. I also allowed the digits after the first character of ID. I also expanded NUM to be able to have at most one decimal point with digits required after the dot. Whitespace and other inputs that were not valid were also ignored and raised the required ScannerException.

### Conceptual: Explain how your implementation aligns with the naive scanner design.

It aligns with the naive scanner because it uses the stringstream with character comparison and consumes inputs from left to right. The token() returns Lexeme and none at the end of file and also throws/raises errors.

### Experiments: Report your timing results for 10/100/1000/10000 tokens and how you ran them.

I ran the scanner on the different test files that were given (10/100/1000/10000/part1). The timing results were 0.0003857612609863281,0.0066411495208740234,0.05184459686279297, -4.521060466766357, and  0.00015282630920410156 respectively. I used the command that we were told to use so "python3 NaiveScanner.py "test file" -v. 

### Explanation: Summarize your implementation choices and discuss performance.

I made sure to keep in mind that ++ and + should differ and that ++ should be noticed before +. I also made sure that invalid decimals were rejected/an error was raised. Since the characters are consumed once, the runtime seems to be linear.

## Part 2

### Submission: Summarize what you submitted in tokens.py and where it lives in your repo.

The Token enum, token actions, and Lexeme are in the tokens.py. As well as the tokens list of Token, regex, and action tuples. In order to handle keywords, I rewrote ID tokens using an action. 

### Written Report: Describe your RE definitions and include timing results for the EM scanner.

The regular expressions I wrote expressed ID as A-Za-z A-Za-z0-9*]. Num was expressed as integer or decimal with digits needed after the ".". HNUM was represented as 0 xX 0-9a-fA-F +. I timed the EM scanner using the 10/100/part2 test files and the times were 0.03647041320800781, 3.8618223667144775,  0.16165971755981445 respectively.

### Testing and Verification: Explain how you tested part2.txt (locally and on Gradescope) and report the outcomes.

In order to test my code I created seperate files one that had tests that all should pass and another that had tests that should fail (raise ScannerException). I debugged using the specific tokens they would fail.

### Debugging and Iteration: Describe any failures you encountered and how you resolved them (include submission iterations if relevant).

I fixed the ++ splitting by making sure INCE had priority and I also made sure to have NUM reje
ct the trailing and multiple decimal points.

## Part 3

### Correctness: Describe how your SOS scanner implements the required behavior, including tricky cases.

I used re.match in order to match the start of the remaining input and then consume the match. I applied the token action and returned None if end of file or raised ScannerException if nothing matched.

### Conceptual: Explain how your design matches the SOS scanning approach.

It matches because each time token() is called. It tests patterns that are only at the current starting position. The priority of tokens is also controlled by the list order. 

### Experiments: Report timings for 10/100/1000/10000 tokens and compare to the EM scanner.

I timed the scanner using the test files that were given. The timings were 0.001855611801147461, 0.0072820186614990234,0.04193520545959473, -5.577428340911865 respectively. The SOS scanner was faster since it used regex less.

### Explanation: Summarize implementation details and performance observations.

The SOS scanner does a re.match for each token definition for each call and it isn't as expensive as anEM scanner because it doesn't use a fullmatch approach. It is more of a simple scanner.

## Part 4

### Correctness: Describe how your NG scanner implements the required behavior, including tricky cases.

The NG scanner has one main regex with groups that are named for all tokens and it runs a match per token() call. It then uses the lastgroup to select the token or action. It skips what is ignored and raises an exception if something is invalid.

### Conceptual: Explain how your design matches the NG scanning approach.

A single combined regex is used compared to using multiple different patterns, which is why it matches the NG scanning approach. Priority is shown through the order of the main group. 

### Experiments: Report timings for 10/100/1000/10000 tokens and compare to the SOS scanner.

I used the 10/100/1000/10000 test files that were given. The timings were   0.0025472640991210938, 0.0020639896392822266, 0.009950876235961914,  0.2071516513824463 respectively. The NG scanner is faster than the SOS scanner because it uses one regex match for each token. 

### Explanation: Summarize implementation details and performance observations.

Having a cached combined regex group lessens the amount of calls and having named groups makes it easier to map the matched to the token types/actions.

