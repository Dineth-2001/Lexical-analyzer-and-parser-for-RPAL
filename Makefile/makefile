# Makefile for RPAL Project by Team Vortex
# Automates running the Python-based RPAL interpreter.
# Date: 02:23 PM +0530, Monday, June 02, 2025

# Default target: run the main program with a default input file
all: run

# Target to run the RPAL interpreter with a default input file (e.g., Q1.txt)
# Uses Windows-style path as specified: python .\myrpal.py file_name
run:
	python .\myrpal.py Inputs\Q1.txt

# Target to run with AST output using the -ast switch
# Prints only the abstract syntax tree as required
run-ast:
	python .\myrpal.py Inputs\Q1.txt -ast

# Target to install dependencies 
setup:
	@echo "No external dependencies required for this project."

# Target to clean up generated files (e.g., Python cache files)
clean:
	rm -rf __pycache__ */__pycache__ *.pyc */*.pyc

# Phony targets (not associated with actual files)
.PHONY: all run run-ast setup clean