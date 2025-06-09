# Makefile for RPAL Project by Team Vortex
# Used for testing the Python-based RPAL interpreter.
# Date: 02:23 PM +0530, Monday, June 05, 2025

# Default target: run the main program with a default input file
all: run

# Target to run the RPAL interpreter with a default input file (e.g., Q1)
# Uses Windows-style path as specified: python .\myrpal.py file_name
run:
	python3 ./myrpal.py Inputs/Q1
	python3 ./myrpal.py Inputs/Q2
	python3 ./myrpal.py Inputs/Q3
	python3 ./myrpal.py Inputs/Q4
	python3 ./myrpal.py Inputs/Q5
	python3 ./myrpal.py Inputs/Q6
	python3 ./myrpal.py Inputs/Q7
	python3 ./myrpal.py Inputs/Q8
	python3 ./myrpal.py Inputs/Q9
	python3 ./myrpal.py Inputs/Q10
	python3 ./myrpal.py Inputs/Q11
	python3 ./myrpal.py Inputs/Q12
	python3 ./myrpal.py Inputs/Q13
	python3 ./myrpal.py Inputs/Q14
	python3 ./myrpal.py Inputs/Q15
	python3 ./myrpal.py Inputs/Q16
	python3 ./myrpal.py Inputs/Q17
	python3 ./myrpal.py Inputs/Q18
	python3 ./myrpal.py Inputs/Q19
	python3 ./myrpal.py Inputs/Q20
	python3 ./myrpal.py Inputs/Q21
	python3 ./myrpal.py Inputs/Q22
	python3 ./myrpal.py Inputs/Q23
	python3 ./myrpal.py Inputs/Q24
	python3 ./myrpal.py Inputs/Q25
	python3 ./myrpal.py Inputs/Q26
	python3 ./myrpal.py Inputs/Q27
	python3 ./myrpal.py Inputs/Q28
	python3 ./myrpal.py Inputs/Q29
	python3 ./myrpal.py Inputs/Q30
	python3 ./myrpal.py Inputs/Q31
	python3 ./myrpal.py Inputs/Q32
	python3 ./myrpal.py Inputs/Q33
	python3 ./myrpal.py Inputs/Q34
	python3 ./myrpal.py Inputs/Q35
	python3 ./myrpal.py Inputs/Q36
	python3 ./myrpal.py Inputs/Q37
	python3 ./myrpal.py Inputs/Q38
	python3 ./myrpal.py Inputs/Q39
	python3 ./myrpal.py Inputs/Q40
	python3 ./myrpal.py Inputs/Q41
	python3 ./myrpal.py Inputs/Q42
	python3 ./myrpal.py Inputs/Q43
	python3 ./myrpal.py Inputs/Q44
	python3 ./myrpal.py Inputs/Q45
	python3 ./myrpal.py Inputs/Q46
	python3 ./myrpal.py Inputs/Q47
	python3 ./myrpal.py Inputs/Q48
	python3 ./myrpal.py Inputs/Q49
	python3 ./myrpal.py Inputs/Q50
	python3 ./myrpal.py Inputs/Q51
	python3 ./myrpal.py Inputs/Q52
	python3 ./myrpal.py Inputs/Q53
	python3 ./myrpal.py Inputs/Q54
	python3 ./myrpal.py Inputs/Q55
	python3 ./myrpal.py Inputs/Q56
	python3 ./myrpal.py Inputs/Q57
	python3 ./myrpal.py Inputs/Q58
	python3 ./myrpal.py Inputs/Q59
	python3 ./myrpal.py Inputs/Q60
	python3 ./myrpal.py Inputs/Q61
	python3 ./myrpal.py Inputs/Q62
	python3 ./myrpal.py Inputs/Q63
	python3 ./myrpal.py Inputs/Q64
	python3 ./myrpal.py Inputs/Q65
	python3 ./myrpal.py Inputs/Q66
	python3 ./myrpal.py Inputs/Q67
	python3 ./myrpal.py Inputs/Q68

# Target to run with AST output using the -ast switch
# Prints only the abstract syntax tree as required
run-ast:
	python3 ./myrpal.py -ast Inputs/Q1
	python3 ./myrpal.py -ast Inputs/Q2
	python3 ./myrpal.py -ast Inputs/Q3
	python3 ./myrpal.py -ast Inputs/Q4
	python3 ./myrpal.py -ast Inputs/Q5
	python3 ./myrpal.py -ast Inputs/Q6
	python3 ./myrpal.py -ast Inputs/Q7
	python3 ./myrpal.py -ast Inputs/Q8
	python3 ./myrpal.py -ast Inputs/Q9
	python3 ./myrpal.py -ast Inputs/Q10
	python3 ./myrpal.py -ast Inputs/Q11
	python3 ./myrpal.py -ast Inputs/Q12
	python3 ./myrpal.py -ast Inputs/Q13
	python3 ./myrpal.py -ast Inputs/Q14
	python3 ./myrpal.py -ast Inputs/Q15
	python3 ./myrpal.py -ast Inputs/Q16
	python3 ./myrpal.py -ast Inputs/Q17
	python3 ./myrpal.py -ast Inputs/Q18
	python3 ./myrpal.py -ast Inputs/Q19
	python3 ./myrpal.py -ast Inputs/Q20
	python3 ./myrpal.py -ast Inputs/Q21
	python3 ./myrpal.py -ast Inputs/Q22
	python3 ./myrpal.py -ast Inputs/Q23
	python3 ./myrpal.py -ast Inputs/Q24
	python3 ./myrpal.py -ast Inputs/Q25
	python3 ./myrpal.py -ast Inputs/Q26
	python3 ./myrpal.py -ast Inputs/Q27
	python3 ./myrpal.py -ast Inputs/Q28
	python3 ./myrpal.py -ast Inputs/Q29
	python3 ./myrpal.py -ast Inputs/Q30
	python3 ./myrpal.py -ast Inputs/Q31
	python3 ./myrpal.py -ast Inputs/Q32
	python3 ./myrpal.py -ast Inputs/Q33
	python3 ./myrpal.py -ast Inputs/Q34
	python3 ./myrpal.py -ast Inputs/Q35
	python3 ./myrpal.py -ast Inputs/Q36
	python3 ./myrpal.py -ast Inputs/Q37
	python3 ./myrpal.py -ast Inputs/Q38
	python3 ./myrpal.py -ast Inputs/Q39
	python3 ./myrpal.py -ast Inputs/Q40
	python3 ./myrpal.py -ast Inputs/Q41
	python3 ./myrpal.py -ast Inputs/Q42
	python3 ./myrpal.py -ast Inputs/Q43
	python3 ./myrpal.py -ast Inputs/Q44
	python3 ./myrpal.py -ast Inputs/Q45
	python3 ./myrpal.py -ast Inputs/Q46
	python3 ./myrpal.py -ast Inputs/Q47
	python3 ./myrpal.py -ast Inputs/Q48
	python3 ./myrpal.py -ast Inputs/Q49
	python3 ./myrpal.py -ast Inputs/Q50
	python3 ./myrpal.py -ast Inputs/Q51
	python3 ./myrpal.py -ast Inputs/Q52
	python3 ./myrpal.py -ast Inputs/Q53
	python3 ./myrpal.py -ast Inputs/Q54
	python3 ./myrpal.py -ast Inputs/Q55
	python3 ./myrpal.py -ast Inputs/Q56
	python3 ./myrpal.py -ast Inputs/Q57
	python3 ./myrpal.py -ast Inputs/Q58
	python3 ./myrpal.py -ast Inputs/Q59
	python3 ./myrpal.py -ast Inputs/Q60
	python3 ./myrpal.py -ast Inputs/Q61
	python3 ./myrpal.py -ast Inputs/Q62
	python3 ./myrpal.py -ast Inputs/Q63
	python3 ./myrpal.py -ast Inputs/Q64
	python3 ./myrpal.py -ast Inputs/Q65
	python3 ./myrpal.py -ast Inputs/Q66
	python3 ./myrpal.py -ast Inputs/Q67
	python3 ./myrpal.py -ast Inputs/Q68

# Target to run with AST output using the -st switch
# Prints only the ST
run-st:
	python3 ./myrpal.py -st Inputs/Q1
	python3 ./myrpal.py -st Inputs/Q2
	python3 ./myrpal.py -st Inputs/Q3
	python3 ./myrpal.py -st Inputs/Q4
	python3 ./myrpal.py -st Inputs/Q5
	python3 ./myrpal.py -st Inputs/Q6
	python3 ./myrpal.py -st Inputs/Q7
	python3 ./myrpal.py -st Inputs/Q8
	python3 ./myrpal.py -st Inputs/Q9
	python3 ./myrpal.py -st Inputs/Q10
	python3 ./myrpal.py -st Inputs/Q11
	python3 ./myrpal.py -st Inputs/Q12
	python3 ./myrpal.py -st Inputs/Q13
	python3 ./myrpal.py -st Inputs/Q14
	python3 ./myrpal.py -st Inputs/Q15
	python3 ./myrpal.py -st Inputs/Q16
	python3 ./myrpal.py -st Inputs/Q17
	python3 ./myrpal.py -st Inputs/Q18
	python3 ./myrpal.py -st Inputs/Q19
	python3 ./myrpal.py -st Inputs/Q20
	python3 ./myrpal.py -st Inputs/Q21
	python3 ./myrpal.py -st Inputs/Q22
	python3 ./myrpal.py -st Inputs/Q23
	python3 ./myrpal.py -st Inputs/Q24
	python3 ./myrpal.py -st Inputs/Q25
	python3 ./myrpal.py -st Inputs/Q26
	python3 ./myrpal.py -st Inputs/Q27
	python3 ./myrpal.py -st Inputs/Q28
	python3 ./myrpal.py -st Inputs/Q29
	python3 ./myrpal.py -st Inputs/Q30
	python3 ./myrpal.py -st Inputs/Q31
	python3 ./myrpal.py -st Inputs/Q32
	python3 ./myrpal.py -st Inputs/Q33
	python3 ./myrpal.py -st Inputs/Q34
	python3 ./myrpal.py -st Inputs/Q35
	python3 ./myrpal.py -st Inputs/Q36
	python3 ./myrpal.py -st Inputs/Q37
	python3 ./myrpal.py -st Inputs/Q38
	python3 ./myrpal.py -st Inputs/Q39
	python3 ./myrpal.py -st Inputs/Q40
	python3 ./myrpal.py -st Inputs/Q41
	python3 ./myrpal.py -st Inputs/Q42
	python3 ./myrpal.py -st Inputs/Q43
	python3 ./myrpal.py -st Inputs/Q44
	python3 ./myrpal.py -st Inputs/Q45
	python3 ./myrpal.py -st Inputs/Q46
	python3 ./myrpal.py -st Inputs/Q47
	python3 ./myrpal.py -st Inputs/Q48
	python3 ./myrpal.py -st Inputs/Q49
	python3 ./myrpal.py -st Inputs/Q50
	python3 ./myrpal.py -st Inputs/Q51
	python3 ./myrpal.py -st Inputs/Q52
	python3 ./myrpal.py -st Inputs/Q53
	python3 ./myrpal.py -st Inputs/Q54
	python3 ./myrpal.py -st Inputs/Q55
	python3 ./myrpal.py -st Inputs/Q56
	python3 ./myrpal.py -st Inputs/Q57
	python3 ./myrpal.py -st Inputs/Q58
	python3 ./myrpal.py -st Inputs/Q59
	python3 ./myrpal.py -st Inputs/Q60
	python3 ./myrpal.py -st Inputs/Q61
	python3 ./myrpal.py -st Inputs/Q62
	python3 ./myrpal.py -st Inputs/Q63
	python3 ./myrpal.py -st Inputs/Q64
	python3 ./myrpal.py -st Inputs/Q65
	python3 ./myrpal.py -st Inputs/Q66
	python3 ./myrpal.py -st Inputs/Q67
	python3 ./myrpal.py -st Inputs/Q68

# Target to run with code using the -l switch
# Prints only the code
run-l:
	python3 ./myrpal.py -l Inputs/Q1
	python3 ./myrpal.py -l Inputs/Q2
	python3 ./myrpal.py -l Inputs/Q3
	python3 ./myrpal.py -l Inputs/Q4
	python3 ./myrpal.py -l Inputs/Q5
	python3 ./myrpal.py -l Inputs/Q6
	python3 ./myrpal.py -l Inputs/Q7
	python3 ./myrpal.py -l Inputs/Q8
	python3 ./myrpal.py -l Inputs/Q9
	python3 ./myrpal.py -l Inputs/Q10
	python3 ./myrpal.py -l Inputs/Q11
	python3 ./myrpal.py -l Inputs/Q12
	python3 ./myrpal.py -l Inputs/Q13
	python3 ./myrpal.py -l Inputs/Q14
	python3 ./myrpal.py -l Inputs/Q15
	python3 ./myrpal.py -l Inputs/Q16
	python3 ./myrpal.py -l Inputs/Q17
	python3 ./myrpal.py -l Inputs/Q18
	python3 ./myrpal.py -l Inputs/Q19
	python3 ./myrpal.py -l Inputs/Q20
	python3 ./myrpal.py -l Inputs/Q21
	python3 ./myrpal.py -l Inputs/Q22
	python3 ./myrpal.py -l Inputs/Q23
	python3 ./myrpal.py -l Inputs/Q24
	python3 ./myrpal.py -l Inputs/Q25
	python3 ./myrpal.py -l Inputs/Q26
	python3 ./myrpal.py -l Inputs/Q27
	python3 ./myrpal.py -l Inputs/Q28
	python3 ./myrpal.py -l Inputs/Q29
	python3 ./myrpal.py -l Inputs/Q30
	python3 ./myrpal.py -l Inputs/Q31
	python3 ./myrpal.py -l Inputs/Q32
	python3 ./myrpal.py -l Inputs/Q33
	python3 ./myrpal.py -l Inputs/Q34
	python3 ./myrpal.py -l Inputs/Q35
	python3 ./myrpal.py -l Inputs/Q36
	python3 ./myrpal.py -l Inputs/Q37
	python3 ./myrpal.py -l Inputs/Q38
	python3 ./myrpal.py -l Inputs/Q39
	python3 ./myrpal.py -l Inputs/Q40
	python3 ./myrpal.py -l Inputs/Q41
	python3 ./myrpal.py -l Inputs/Q42
	python3 ./myrpal.py -l Inputs/Q43
	python3 ./myrpal.py -l Inputs/Q44
	python3 ./myrpal.py -l Inputs/Q45
	python3 ./myrpal.py -l Inputs/Q46
	python3 ./myrpal.py -l Inputs/Q47
	python3 ./myrpal.py -l Inputs/Q48
	python3 ./myrpal.py -l Inputs/Q49
	python3 ./myrpal.py -l Inputs/Q50
	python3 ./myrpal.py -l Inputs/Q51
	python3 ./myrpal.py -l Inputs/Q52
	python3 ./myrpal.py -l Inputs/Q53
	python3 ./myrpal.py -l Inputs/Q54
	python3 ./myrpal.py -l Inputs/Q55
	python3 ./myrpal.py -l Inputs/Q56
	python3 ./myrpal.py -l Inputs/Q57
	python3 ./myrpal.py -l Inputs/Q58
	python3 ./myrpal.py -l Inputs/Q59
	python3 ./myrpal.py -l Inputs/Q60
	python3 ./myrpal.py -l Inputs/Q61
	python3 ./myrpal.py -l Inputs/Q62
	python3 ./myrpal.py -l Inputs/Q63
	python3 ./myrpal.py -l Inputs/Q64
	python3 ./myrpal.py -l Inputs/Q65
	python3 ./myrpal.py -l Inputs/Q66
	python3 ./myrpal.py -l Inputs/Q67
	python3 ./myrpal.py -l Inputs/Q68

# Target to install dependencies 
setup:
	@echo "No external dependencies required for this project."

# Target to clean up generated files (e.g., Python cache files)
clean:
	rm -rf __pycache__ */__pycache__ *.pyc */*.pyc

# Phony targets (not associated with actual files)
.PHONY: all run run-ast setup clean
