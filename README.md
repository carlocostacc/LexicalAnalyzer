# LexicalAnalyzer
begging of a compiler


Project: Simple Lexical Analyzer

1. Description
   This project is a basic lexer that scans an input file for tokens
   such as identifiers, integers, floats, operators, and comments. 
   Invalid or unrecognized sequences are reported as errors.

2. Required Input File
   You must create a file named `input.txt` in the same directory 
   as the lexer (the main.py script). Place any code or sample input 
   you want the lexer to process in `input.txt`.

3. How to Run
   - Ensure you have Python 3 installed.
   - Open a terminal or command prompt in this project's directory.
   - Run the lexer with: `python main.py`
   - The lexer will read `input.txt` and produce two output files:
     - `outlextokens.txt` for valid tokens
     - `outlexerrors.txt` for errors

4. Notes
   - If `input.txt` is missing or cannot be opened, the program will 
     print an error message and exit.
   - The lexer stops reading when it reaches the end of `input.txt`.

5. Contact
   If you have questions or need further assistance, please reach out 
   to the project maintainer.
