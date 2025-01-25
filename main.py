from __future__ import print_function
import sys
import os

# following two must remain in the same order

tk_Id, tk_Int, tk_Float, tk_Frac, tk_Letter, tk_Digit, tk_Nonzero, tk_alphanum,  \
tk_Eq, tk_Neq, tk_Lss, tk_Gtr, tk_Leq, tk_Geq, \
tk_Add, tk_Sub, tk_Mul, tk_Div, tk_Not, tk_And, tk_Or, \
tk_Assign, \
tk_Lparen, tk_Rparen, tk_Lbrace, tk_Rbrace, tk_LeftBracket, tk_RightBracket, tk_Semi, tk_Comma, tk_Dot, tk_Colon, \
tk_Arrow, \
tk_Keyword_int, tk_Keyword_float, tk_Keyword_void, tk_Keyword_class, tk_Keyword_self, tk_Keyword_isa, \
tk_Keyword_implementation, tk_While, tk_If, tk_Then, tk_Else, tk_Read, tk_Write, tk_Return, tk_Local, \
tk_Constructor, tk_Attribute, tk_Function, tk_Public, tk_Private, \
tk_Open_block_comment, tk_Close_block_comment, tk_Line_comment, tk_Err = range(57)

# the tk_Err is the error token when ever we see an incorrect character or symbol the error token will be returned


all_syms = [
    # Atomic Lexical Elements
    "id",          # For identifiers
    "int",         # Integer numbers
    "float",       # Floating-point numbers

    "fraction",    #fraction i dont thing the e thing will be implemented
    "letter",      #letter
    "digit",       #nuber with one digit
    "nonzero",     # integer that is non zero
    "alphanum",

    # Relational Operators
    "Op_equal",    # ==
    "Op_notequal", # <>
    "Op_less",     # <
    "Op_greater",  # >
    "Op_lessequal",# <=
    "Op_greaterequal", # >=

    # Arithmetic Operators
    "Op_add",      # +
    "Op_subtract", # -
    "Op_multiply", # *
    "Op_divide",   # /
    "Op_not",      # not
    "Op_and",      # and
    "Op_or",       # or

    # Assignment
    "Op_assign",   # :=

    # Punctuation
    "LeftParen",   # (
    "RightParen",  # )
    "LeftBrace",   # {
    "RightBrace",  # }
    "LeftBracket", # [
    "RightBracket",# ]
    "Semicolon",   # ;
    "Comma",       # ,
    "Dot",         # .
    "Colon",       # :

    # Special Constructs
    "Arrow",       # =>

    # all symbols done 

    # Reserved Words (Keywords)
    "Keyword_int",          # int
    "Keyword_float",        # float
    "Keyword_void",         # void
    "Keyword_class",        # class
    "Keyword_self",         # self
    "Keyword_isa",          # isa
    "Keyword_implementation", # implementation
    "Keyword_while",        # while
    "Keyword_if",           # if
    "Keyword_then",         # then
    "Keyword_else",         # else
    "Keyword_read",         # read
    "Keyword_write",        # write
    "Keyword_return",       # return
    "Keyword_local",        # local
    "Keyword_constructor",  # constructor
    "Keyword_attribute",    # attribute
    "Keyword_function",     # function
    "Keyword_public",       # public
    "Keyword_private",      # private
    # done

    "Open_block_comment",         # open comment /*
    "Close_block_comment",         # close comment *\
    "Line_comment",          #line comment //

    "error" 

]

key_words = {tk_Keyword_int : "int", tk_Keyword_float: "float", tk_Keyword_void: "void", tk_Keyword_class: "class", tk_Keyword_self : "self", tk_Keyword_isa: "isa", \
tk_Keyword_implementation : "implementation", tk_While: "while", tk_If: "if", tk_Then:"then", tk_Else:"else", tk_Read:"read", tk_Write:"write", tk_Return:"return", tk_Local:"local", \
tk_Constructor: "constructor", tk_Attribute: "attribute", tk_Function: "function", tk_Public: "public", tk_Private:"private",tk_Not:"not", tk_And:"and", tk_Or:"or"}

# single character only symbols
symbols = { '{': tk_Lbrace, '}': tk_Rbrace, '(': tk_Lparen, ')': tk_Rparen, '+': tk_Add, '-': tk_Sub,
    '*': tk_Mul, '.': tk_Dot, ';': tk_Semi, ',': tk_Comma, ':': tk_Colon, '[': tk_LeftBracket, ']': tk_RightBracket }

the_ch = " "    # dummy first char - but it must be a space
the_col = 0
the_line = 1
input_file = None  # set once we open a file

#letter list containing upper and lower case letters of the alphabet
letter = [chr(i) for i in range(97, 123)] + [chr(i) for i in range(65, 91)]

# # File paths for output
# ERROR_FILE = "outlexerrors.txt"
# TOKEN_FILE = "outlextokens.txt"

# # Initialize files (clear contents before writing)
# open(ERROR_FILE, "w").close()
# open(TOKEN_FILE, "w").close()

def write_to_file(filename, content):
    """Append content to a specified file."""
    with open(filename, "a") as file:
        file.write(content + "\n")

#*** show error and exit  TODO need to do better error handling
def error(line, col, msg):
    print(line, col, msg)


# try:
#     # Always attempt to open "input.txt" in read mode
#     input_file = open("input.txt", "r", 4096)
# except IOError as e:
#     # If the file cannot be opened, report an error and exit
#     error(0, 0, f"Can't open input.txt: {e}")
#     sys.exit(1)



#*** get the next character from the input
def next_ch():
    global the_ch, the_col, the_line

    the_ch = input_file.read(1)
    the_col += 1
    if the_ch == '\n':
        the_line += 1
        the_col = 0
    return the_ch

#letter
def char_lit(start, err_line, err_col):
    global the_ch
    text = ""

    # Read the first character inside the single quotes
    next_ch()
    if the_ch == '\\':  # Handle escape sequences
        next_ch()
        if the_ch not in ['n', 't', '\\', '\'', '"']:
            error(err_line, err_col, f"escape sequence unknown \\{the_ch}")
        text = '\\' + the_ch
    else:
        text = the_ch

    next_ch()  # Move past the character or escape sequence

    # Ensure the next character is the closing single quote
    if the_ch != start:
        error(err_line, err_col, "EOF or multiple characters in character literal")

    next_ch()  # Move past the closing single quote
    return tk_Letter, err_line, err_col, text

#*** handle identifiers and integers
def ident_or_int(err_line, err_col):
    global the_ch
    text = ""
    is_number = True

    while the_ch.isalnum() or the_ch == '_':
        if not the_ch.isdigit():
            is_number = False
        text += the_ch
        next_ch()

    # Check for leading zeros (invalid if length > 1)
    if text.startswith('0') and len(text) > 1:
        error(err_line, err_col, f"Invalid number: leading zeros not allowed ({text})")
        err_msg = f"Invalid number: leading zeros not allowed ({text})"
        return tk_Err, err_line, err_col, err_msg

    # If every character was a digit, it's an integer
    if is_number:
        # Safely attempt to convert to int
        try:
            val = int(text)
        except ValueError:
            # If 'text' is empty or otherwise invalid for int()
            error(err_line, err_col, f"Invalid integer literal: ({text})")
            err_msg = f"Invalid integer literal: ({text})"
            next_ch()
            return tk_Err, err_line, err_col, err_msg
        return tk_Int, err_line, err_col, val

    # If it starts with a digit or underscore, it's an invalid identifier
    if text[0].isdigit() or text[0] == '_':
        err_msg = f"Invalid identifier: {text}"
        error(err_line, err_col, f"Invalid identifier: {text}")
        return tk_Err, err_line, err_col, err_msg

    # Check if the text is a keyword by comparing against key_words dictionary values
    # (Since key_words maps token_code -> string, we iterate to find a match)
    for tk_code, kw_lex in key_words.items():
        if kw_lex == text:
            # It's a keyword
            return tk_code, err_line, err_col

    # Otherwise, it's a valid identifier
    return tk_Id, err_line, err_col, text

def scan_number(err_line, err_col):
    """
    Reads a numeric token (int or float with optional exponent).
    Returns (token_code, line, col, value).
    """
    global the_ch
    text = ""

    # 1) Read initial digits
    while the_ch.isdigit():
        text += the_ch
        next_ch()

    # 2) Check for decimal point
    if the_ch == '.':
        text += the_ch
        next_ch()
        # read any digits after the decimal
        while the_ch.isdigit():
            text += the_ch
            next_ch()

    # 3) Check for exponent
    if the_ch in ['e','E']:
        text += the_ch
        next_ch()
        # optional sign
        if the_ch in ['+','-']:
            text += the_ch
            next_ch()

        # read exponent digits
        if not the_ch.isdigit():
            err_msg = f"Invalid float exponent: {text}"
            error(err_line, err_col, err_msg)
            return tk_Err, err_line, err_col, err_msg
        
        while the_ch.isdigit():
            text += the_ch
            next_ch()

    # Now `text` might look like "34", "34.5", "34e2", "34.5e-1", etc.

    # 4) Decide if it's int or float
    if '.' in text or 'e' in text or 'E' in text:
        # parse float, watch for trailing zero logic if you want
        # your existing trailing-zero checks, etc.
        try:
            # optional trailing zero logic, exponent checks, etc.
            value = float(text)
        except ValueError:
            err_msg = f"Invalid float literal: {text}"
            error(err_line, err_col, err_msg)
            return tk_Err, err_line, err_col, err_msg
        return tk_Float, err_line, err_col, value
    else:
        # parse int
        try:
            value = int(text)
        except ValueError:
            err_msg = f"Invalid integer literal: {text}"
            error(err_line, err_col, err_msg)
            return tk_Err, err_line, err_col, err_msg

        return tk_Int, err_line, err_col, value



#*** handle floating-point literals
def float_lit(start, err_line, err_col):
    global the_ch
    text = start
    has_dot = start == '.'
    has_exponent = False

    while True:
        next_ch()
        if the_ch.isdigit():
            text += the_ch
        elif the_ch == '.' and not has_dot:
            has_dot = True
            text += the_ch
        elif the_ch in 'eE' and not has_exponent:
            has_exponent = True
            text += the_ch
            next_ch()
            if the_ch in '+-':
                text += the_ch
                next_ch()
            continue
        else:
            break

    if '.' not in text and not has_exponent:
        error(err_line, err_col, f"Invalid float literal: {text}")
        err_msg = f"Invalid float literal: {text}"
        return tk_Err, err_line, err_col, err_msg

    fraction_part = text.split('.')[-1] if '.' in text else ""
    if fraction_part.endswith('0') and len(fraction_part) > 1:
        error(err_line, err_col, f"Invalid float literal (trailing zero): {text}")
        err_msg = f"Invalid float literal (trailing zero): {text}"
        return tk_Err, err_line, err_col, err_msg

    return tk_Float, err_line, err_col, float(text)

#*** look ahead for '>=', etc.
def follow(expect, ifyes, ifno, err_line, err_col):
    if next_ch() == expect:
        next_ch()
        return ifyes, err_line, err_col

    if ifno == tk_Err:
        error(err_line, err_col, "follow: unrecognized character: (%d) '%c'" % (ord(the_ch), the_ch))

    return ifno, err_line, err_col

#*** return the next token type
def gettok():
    # Skip whitespace
    global the_ch
    while the_ch.isspace():
        next_ch()

    err_line = the_line
    err_col  = the_col
    # Check for end of file
    if len(the_ch) == 0:    return tk_Err, err_line, err_col, "EOF reached"

    # 1) Handle '/' for division or comments
    if the_ch == '/':
        ch2 = next_ch()  # Look at the next character
        if ch2 == '*':
            # We saw "/*" => open block comment
            next_ch()  # consume after '*'
            return tk_Open_block_comment, err_line, err_col
        elif ch2 == '/':
            # We saw "//" => line comment
            next_ch()  # consume after second '/'
            return tk_Line_comment, err_line, err_col
        else:
            # It's just a division symbol
            the_ch = ch2
            return tk_Div, err_line, err_col

    # 1.1) handle of closing block comment
    if the_ch == '*':
        ch2 = next_ch()
        if ch2 == '/':
            # '*/'
            next_ch()
            return tk_Close_block_comment, err_line, err_col
        else:
            the_ch = ch2
            return tk_Mul, err_line, err_col

    # 2) Handle '<' for '<', '<=', '<>'        
    if the_ch == '<':
        ch2 = next_ch()
        if ch2 == '=':
            # '<='
            next_ch()
            return tk_Leq, err_line, err_col
        elif ch2 == '>':
            # '<>'
            next_ch()
            return tk_Neq, err_line, err_col
        else:
            # Just '<'
            return tk_Lss, err_line, err_col

    # 3) Handle '>' for '>', '>='
    if the_ch == '>':
        ch2 = next_ch()
        if ch2 == '=':
            next_ch()
            return tk_Geq, err_line, err_col
        else:
            return tk_Gtr, err_line, err_col


    # 5) Handle '=' for '=', '==', '=>', ':='
    if the_ch == '=':
        ch2 = next_ch()
        if ch2 == '=':
            next_ch()
            return tk_Eq, err_line, err_col
        elif ch2 == '>':
            # '=>'
            next_ch()
            return tk_Arrow, err_line, err_col
        else:
            # single = are not supported by the lexime
            err_msg = "Invalid single '=' usage"
            return tk_Err, err_line, err_col, err_msg

    # 6) Handle ':' for ':' or ':=' 
    if the_ch == ':':
        ch2 = next_ch()
        if ch2 == '=':
            next_ch()
            return tk_Assign, err_line, err_col
        else:
            return tk_Colon, err_line, err_col

    # 7) Handle any single-character symbols (e.g. +, -, (, ), etc.)
    if the_ch in symbols:
        sym = symbols[the_ch]
        next_ch()
        return sym, err_line, err_col
    
     # 8) Handle digit => integer or float
    if the_ch.isdigit():
        return scan_number(err_line, err_col)

    # 9) Handle '.' => float        
    if the_ch == '.':
        return float_lit('.', err_line, err_col)

    # 10) Otherwise, it could be an identifier or integer with a leading alpha/underscore
    return ident_or_int(err_line, err_col)

#*** main driver
# input_file = sys.stdin
# if len(sys.argv) > 1:
#     try:
#         input_file = open(sys.argv[1], "r", 4096)
#     except IOError as e:
#         error(0, 0, "Can't open %s" % sys.argv[1])

def process_file(input_path, out_errors_path, out_tokens_path):
    """Processes a single file, writing errors/tokens to separate files."""
    global input_file, the_ch, the_line, the_col

    # Reset lexical counters
    the_line = 1
    the_col = 0
    the_ch = " "

    try:
        input_file = open(input_path, "r", 4096)
    except IOError as e:
        print(f"Can't open {input_path}: {e}")
        return

    # Clear/overwrite any existing output
    open(out_errors_path, "w").close()
    open(out_tokens_path, "w").close()

    # Lexing loop
    while True:
        t = gettok()  # (token_code, line, col, maybeValue)
        tok = t[0]
        line = t[1]
        col = t[2]

        # If we have a 4th element, it's the token's lexeme/value
        if len(t) > 3:
            token_value = str(t[3])
        else:
            token_value = all_syms[tok]  # fallback name

        token_string = f"[{all_syms[tok]}, {token_value}, {line}]"

        if tok == tk_Err:
            # This is an error token
            write_to_file(out_errors_path, token_string)
            print(token_string)
        else:
            # Valid token
            write_to_file(out_tokens_path, token_string)
            print(token_string)

        # If the_ch is empty => EOF => stop
        if len(the_ch) == 0:
            break

    input_file.close()

def main():
    # Directories
    input_dir = "input"
    output_dir = "output"

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over all files in input/
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isdir(input_path):
            continue  # skip subdirectories
        if not filename.endswith(".txt"):
            continue  # skip non-txt files if desired

        # Prepare output filenames
        # e.g. file1.txt => file1_outlexerrors.txt, file1_outlextokens.txt
        base_name = filename.rsplit(".txt", 1)[0]
        out_errors = os.path.join(output_dir, f"{base_name}_outlexerrors.txt")
        out_tokens = os.path.join(output_dir, f"{base_name}_outlextokens.txt")

        print(f"\nProcessing file: {filename}")
        print(f"Errors -> {out_errors}")
        print(f"Tokens -> {out_tokens}")

        process_file(input_path, out_errors, out_tokens)


if __name__ == "__main__":
    main()
