# Lexical-analyzer-and-parser-for-RPAL

This repository contains an interpreter for the RPAL (Right-reference Pedagogical Algorithmic Language) programming language, implemented in Python. The interpreter follows the standard phases of compilation:

## Compilation Phases

* **Lexical Analysis**: Tokenizes source code using the scanner
* **Parsing**: Builds an Abstract Syntax Tree (AST)
* **Standardization**: Transforms the AST into a standardized tree
* **Execution**: Runs the program using a CSE (Control Structure Environment) machine

## Project Structure

```
.
├── cse_machine/           # CSE machine implementation
├── data_structures/       # Common data structures used across the interpreter
├── Inputs/                # Sample RPAL programs
├── parser/                # Parser implementation for building ASTs
├── scanner/               # Scanner/lexer implementation
├── standardiser/          # Standardization phase implementation
├── makefile               # Makefile for running tests and examples
├── myrpal.py              # Main interpreter entry point
└── README.md              # This documentation
```

## Data Structures

* **Node**: Tree structure for AST representation
* **Stack**: Used in parsing and CSE machine
* **Environment**: Manages variable bindings in the CSE machine
* **Control Structures**: Lambda, Delta, Tau, Eta for CSE machine

## Usage

Run the interpreter with:

```bash
python myrpal.py [options] <file_path>
```

### Options

* `-ast`: Display the Abstract Syntax Tree only
* `-st`: Display the Standardized Tree only
* `-l`: Display the input source code only

### Examples

#### Run a program

```bash
python myrpal.py Inputs/Q1.txt
```

#### Show only the AST

```bash
python myrpal.py -ast Inputs/Q1.txt
```

#### Show only the standardized tree

```bash
python myrpal.py -st Inputs/Q1.txt
```

## Using the Makefile

The project includes a Makefile for common operations:

```bash
# Run default program (Q1.txt)
make

# Show AST for default program
make run-ast

# Show standardized tree for default program
make run-st

# Show source code of default program
make run-l

# Clean up Python cache files
make clean
```

## Language Features

The RPAL interpreter supports:

* Functional programming constructs
* Lambda expressions and closures
* Conditionals and pattern matching
* Recursive functions
* Built-in operations for strings, tuples, and arithmetics
* Let/Where expressions
