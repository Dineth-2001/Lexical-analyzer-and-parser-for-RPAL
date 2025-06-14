#!/usr/bin/env python3
# filepath: d:\Sem 04\Programming Languages\Lexical-analyzer-and-parser-for-RPAL\myrpal.py
import sys
import os

from scanner.scanner import tokenize_and_screen
from parser.parser import parse
from standardiser.standardiser import generate_standardized_tree
from cse_machine.cse_machine import get_result

def main():
    # Check for correct number of arguments
    if len(sys.argv) < 2:
        print("Usage: python myrpal.py [-ast] [-st] [-l] <file_path>")
        sys.exit(1)
    
    # Parse switches and find file path
    show_ast = "-ast" in sys.argv
    show_st = "-st" in sys.argv
    show_code = "-l" in sys.argv
    
    # Get file path (the argument that is not a switch)
    file_path = None
    for arg in sys.argv[1:]:
        if not arg.startswith('-'):
            file_path = arg
            break
    
    # Check if file path was found
    if not file_path:
        print("Error: No file path provided")
        print("Usage: python myrpal.py [-ast] [-st] [-l] <file_path>")
        sys.exit(1)
    
    # Check if file exists
    if not os.path.isfile(file_path):
        # Try checking in the Inputs folder
        input_path = os.path.join("Inputs", file_path)
        if os.path.isfile(input_path):
            file_path = input_path
        else:
            print(f"Error: File '{file_path}' not found.")
            sys.exit(1)
    
    # Read code from file
    try:
        with open(file_path, 'r') as file:
            code = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
        
    # If -l switch, just show the code and exit
    if show_code:
        print(code)
        sys.exit(0)
        
    # Step 1: Tokenize
    tokens = tokenize_and_screen(code)
    tokens.reverse()  # Reverse the tokens to use the list as a stack
    
    # Step 2: Parse and build AST
    try:
        ast = parse(tokens)
        
        # If -ast switch, show the AST and exit
        if show_ast:
            ast.print_tree()
            sys.exit(0)
            
        # Step 3: Standardize the tree
        standardized_tree = generate_standardized_tree(ast)
        
        # If -st switch, show the standardized tree and exit
        if show_st:
            standardized_tree.print_tree()
            sys.exit(0)
            
        # Step 4: Generate and run CSE machine code
        print("Output of the above program is:")
        get_result(standardized_tree)
        
            
    except SyntaxError as e:
        print(f"Syntax Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()