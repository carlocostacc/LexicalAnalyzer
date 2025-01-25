README
1. Project Overview

This project is a lexical analyzer that processes multiple input files located in an input/ directory and generates corresponding token and error reports in an output/ directory. Each input file is scanned for valid tokens (integers, floats, identifiers, keywords, etc.), as well as invalid tokens (leading-zero integers, trailing-zero floats, invalid identifiers, and so on).
2. Requirements

    Python 3 installed (the script uses Python 3 features).
    A folder structure that includes:
        A main.py script (the lexer).
        An input/ directory containing one or more .txt files to be scanned.
        An output/ directory, which will hold the generated output files.

3. How to Run

    Place all input files (e.g., file1.txt, file2.txt, etc.) into the input/ directory.
    Open a terminal or command prompt in the same directory as main.py.
    Run the lexer:

python main.py

or, if on Windows with multiple Python versions installed:

    python3 main.py

    The lexer will:
        Enumerate all .txt files in input/.
        For each file named X.txt, produce two files in output/:
            X_outlexerrors.txt (containing detected errors)
            X_outlextokens.txt (listing recognized tokens)
    Check the output/ directory to see the results.
        Each token line is logged as [TokenType, LexemeOrValue, LineNumber].
        Each error line is similarly logged as [error, <message>, LineNumber].

4. Lexical Rules & Examples

    Identifiers: Must start with a letter (a-zA-Z), followed by letters, digits, or underscores (_). Leading digits or _ are disallowed.
    Integers: Disallow leading zeros (e.g., 0123 is invalid). A single 0 is permitted.
    Floats: Recognize optional decimal (.) and exponent parts (e/E plus optional +/-). Trailing zeros in the fraction (e.g., 3.140) are invalid per design.
    Keywords: int, float, while, if, then, else, etc. Any identifier matching these keywords is promoted to a keyword token.
    Comments:
        Single-line: // ... (ends at newline).
        Block: /* ... */.
    Operators: <, >, <=, >=, ==, <>, :=, etc.
    Punctuation: (, ), {, }, [, ], ., ,, ;, etc.
    Errors: Any invalid token, such as leading zeros on integers, underscores leading an identifier, or malformed floats, is logged in the error file.

5. Extending or Modifying

    To add new tokens (operators, punctuation), extend the symbols dictionary or the relevant sections in gettok().
    To change lexical rules (e.g., allow _ at the start of identifiers), modify the logic in ident_or_int() or other specialized functions.
    To alter error-handling or token-logging, adjust the lines inside gettok() and the process_file() function.
