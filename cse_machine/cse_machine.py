from data_structures.stack import Stack
from data_structures.cse_enviroment import Environment
from data_structures.control_structures import Lambda, Delta, Tau, Eta
from scanner.scanner import tokenize_and_screen
from parser.parser import parse
from standardiser.standardiser import generate_standardized_tree


control_structures = []
count = 0
control = []
stack = Stack("CSE")     
environments = [Environment(0, None)]
current_environment = 0
builtInFunctions = ["Order", "Print", "print", "Conc", "Stern", "Stem", "Isinteger", "Istruthvalue", "Isstring", "Istuple", "Isfunction", "ItoS"]
print_present = False


def generate_control_structure(node, index):
    global count

    while len(control_structures) <= index:
        control_structures.append([])

    # Case: Lambda node – starts a new control structure
    if node.value == "lambda":
        count += 1
        lambda_id = count
        param_node = node.children[0]
        lambda_obj = Lambda(lambda_id)

        if param_node.value == ",":
            # Multiple parameters
            bound_vars = ",".join(child.value[4:-1] for child in param_node.children)
        else:
            # Single parameter
            bound_vars = param_node.value[4:-1]

        lambda_obj.bounded_variable = bound_vars
        control_structures[index].append(lambda_obj)

        # Recurse into the body of the lambda
        for child in node.children[1:]:
            generate_control_structure(child, lambda_id)

    # Case: Conditional expression (if-then-else)
    elif node.value == "->":
        count += 1
        then_id = count
        control_structures[index].append(Delta(then_id))
        generate_control_structure(node.children[1], then_id)

        count += 1
        else_id = count
        control_structures[index].append(Delta(else_id))
        generate_control_structure(node.children[2], else_id)

        control_structures[index].append("beta")
        # Recurse into the condition
        generate_control_structure(node.children[0], index)

    # Case: Tuple (tau) node
    elif node.value == "tau":
        tuple_size = len(node.children)
        control_structures[index].append(Tau(tuple_size))
        for child in node.children:
            generate_control_structure(child, index)

    # Default case: simple value or operator
    else:
        control_structures[index].append(node.value)
        for child in node.children:
            generate_control_structure(child, index)

# Resolves tokens enclosed in '<...>' to their actual values.
def lookup(token):
    stripped = token[1:-1]
    parts = stripped.split(":")

    # Handle simple tokens like <Y*>, <true>, <nil>
    if len(parts) == 1:
        key = parts[0]
    else:
        token_type, key = parts[0], parts[1]

        if token_type == "INT":
            return int(key)

        elif token_type == "STR":
            return key.strip("'")

        elif token_type == "ID":
            if key in builtInFunctions:
                return key
            try:
                return environments[current_environment].variables[key]
            except KeyError:
                print(f"Undeclared Identifier: {key}")
                exit(1)

    # Handle special cases
    if key == "Y*":
        return "Y*"
    elif key == "nil":
        return ()
    elif key == "true":
        return True
    elif key == "false":
        return False
    
def built_in(func_name, arg):
    global print_present

    match func_name:
        case "Order":
            # Returns the number of elements in a tuple
            stack.push(len(arg))

        case "Print" | "print":
            print_present = True
            # Replace escape characters with actual formatting
            if isinstance(arg, str):
                arg = arg.replace("\\n", "\n").replace("\\t", "\t")
            print(arg, end="")
            stack.push(arg)

        case "Conc":
            second_str = stack.pop()
            control.pop()
            stack.push(arg + second_str)

        case "Stern":
            # Return string without first character
            stack.push(arg[1:] if isinstance(arg, str) and len(arg) > 0 else "")

        case "Stem":
            # Return first character of string
            stack.push(arg[0] if isinstance(arg, str) and len(arg) > 0 else "")

        case "Isinteger":
            stack.push(isinstance(arg, int))

        case "Istruthvalue":
            stack.push(isinstance(arg, bool))

        case "Isstring":
            stack.push(isinstance(arg, str))

        case "Istuple":
            stack.push(isinstance(arg, tuple))

        case "Isfunction":
            stack.push(arg in builtInFunctions)

        case "ItoS":
            if isinstance(arg, int):
                stack.push(str(arg))
            else:
                print("Error: ItoS function expects an integer.")
                exit(1)

        case _:
            print(f"Unknown built-in function: {func_name}")
            exit(1)

def apply_rules():
    op = ["+", "-", "*", "/", "**", "gr", "ge", "ls", "le", "eq", "ne", "or", "&", "aug"]
    uop = ["neg", "not"]

    global control
    global current_environment

    while(len(control) > 0):
     
        symbol = control.pop()

        # Rule 1
        if type(symbol) == str and (symbol[0] == "<" and symbol[-1] == ">"):
            stack.push(lookup(symbol))

        # Rule 2
        elif type(symbol) == Lambda:
            temp = Lambda(symbol.number)
            temp.bounded_variable = symbol.bounded_variable
            temp.environment = current_environment
            stack.push(temp)

        # Rule 4
        elif (symbol == "gamma"):
            stack_symbol_1 = stack.pop()
            stack_symbol_2 = stack.pop()

            if (type(stack_symbol_1) == Lambda):
                current_environment = len(environments)
                
                lambda_number = stack_symbol_1.number
                bounded_variable = stack_symbol_1.bounded_variable
                parent_environment_number = stack_symbol_1.environment

                parent = environments[parent_environment_number]
                child = Environment(current_environment, parent)
                parent.add_child(child)
                environments.append(child)

                # Rule 11
                variable_list = bounded_variable.split(",")
                
                if (len(variable_list) > 1):
                    for i in range(len(variable_list)):
                        child.add_variable(variable_list[i], stack_symbol_2[i])
                else:
                    child.add_variable(bounded_variable, stack_symbol_2)

                stack.push(child.name)
                control.append(child.name)
                control += control_structures[lambda_number]

            # Rule 10
            elif (type(stack_symbol_1) == tuple):
                stack.push(stack_symbol_1[stack_symbol_2 - 1])

            # Rule 12
            elif (stack_symbol_1 == "Y*"):
                temp = Eta(stack_symbol_2.number)
                temp.bounded_variable = stack_symbol_2.bounded_variable
                temp.environment = stack_symbol_2.environment
                stack.push(temp)

            # Rule 13
            elif (type(stack_symbol_1) == Eta):
                temp = Lambda(stack_symbol_1.number)
                temp.bounded_variable = stack_symbol_1.bounded_variable
                temp.environment = stack_symbol_1.environment
                
                control.append("gamma")
                control.append("gamma")
                stack.push(stack_symbol_2)
                stack.push(stack_symbol_1)
                stack.push(temp)

            # Built-in functions
            elif stack_symbol_1 in builtInFunctions:
                built_in(stack_symbol_1, stack_symbol_2)
              
        # Rule 5
        elif type(symbol) == str and (symbol[0:2] == "e_"):
            stack_symbol = stack.pop()
            stack.pop()
            
            if (current_environment != 0):
                for element in reversed(stack):
                    if (type(element) == str and element[0:2] == "e_"):
                        current_environment = int(element[2:])
                        break
            stack.push(stack_symbol)

        # Rule 6
        elif (symbol in op):
            rand_1 = stack.pop()
            rand_2 = stack.pop()
            if (symbol == "+"): 
                stack.push(rand_1 + rand_2)
            elif (symbol == "-"):
                stack.push(rand_1 - rand_2)
            elif (symbol == "*"):
                stack.push(rand_1 * rand_2)
            elif (symbol == "/"):
                stack.push(rand_1 // rand_2)
            elif (symbol == "**"):
                stack.push(rand_1 ** rand_2)
            elif (symbol == "gr"):
                stack.push(rand_1 > rand_2)
            elif (symbol == "ge"):
                stack.push(rand_1 >= rand_2)
            elif (symbol == "ls"):
                stack.push(rand_1 < rand_2)
            elif (symbol == "le"):
                stack.push(rand_1 <= rand_2)
            elif (symbol == "eq"):
                stack.push(rand_1 == rand_2)
            elif (symbol == "ne"):
                stack.push(rand_1 != rand_2)
            elif (symbol == "or"):
                stack.push(rand_1 or rand_2)
            elif (symbol == "&"):
                stack.push(rand_1 and rand_2)
            elif (symbol == "aug"):
                if (type(rand_2) == tuple):
                    
                    stack.push(rand_1 + rand_2)
                else:
                    stack.push(rand_1 + (rand_2,))

        # Rule 7
        elif (symbol in uop):
            rand = stack.pop()
            if (symbol == "not"):
                stack.push(not rand)
            elif (symbol == "neg"):
                stack.push(-rand)

        # Rule 8
        elif (symbol == "beta"):
            B = stack.pop()
            else_part = control.pop()
            then_part = control.pop()
            if (B):
                control += control_structures[then_part.number]
            else:
                control += control_structures[else_part.number]

        # Rule 9
        elif type(symbol) == Tau:
            n = symbol.number
            tau_list = []
            for i in range(n):
                tau_list.append(stack.pop())
            tau_tuple = tuple(tau_list)
            stack.push(tau_tuple)

        elif (symbol == "Y*"):
            stack.push(symbol)

    # Lambda expression becomes a lambda closure 
    if type(stack[0]) == Lambda:
        stack[0] = "[lambda closure: " + str(stack[0].bounded_variable) + ": " + str(stack[0].number) + "]"
         
    if type(stack[0]) == tuple:          
        # Emulating printing the boolean values in lowercase
        for i in range(len(stack[0])):
            if type(stack[0][i]) == bool:
                stack[0] = list(stack[0])
                stack[0][i] = str(stack[0][i]).lower()
                stack[0] = tuple(stack[0])
                
        # Program does not print the comma when there is only one element in the tuple  
        if len(stack[0]) == 1:
            stack[0] = "(" + str(stack[0][0]) + ")"
        
        # The program does not print inverted commas when an element in the tuple is a string 
        else: 
            if any(type(element) == str for element in stack[0]):
                temp = "("
                for element in stack[0]:
                    temp += str(element) + ", "
                temp = temp[:-2] + ")"
                stack[0] = temp
                
    # The program prints the boolean values in lowercase  
    if stack[0] == True or stack[0] == False:
        stack[0] = str(stack[0]).lower()

def get_result(st):
    global control    
    generate_control_structure(st,0) 
    
    control.append(environments[0].name)
    control += control_structures[0]

    stack.push(environments[0].name)

    apply_rules()

    if print_present:
        return stack[0]
    else:
        return ""

if __name__ == "__main__":
    with open('Inputs/Q.txt', 'r') as file:
        code = file.read()
        tokens = tokenize_and_screen(code)
        tokens.reverse()  # Reverse the tokens 

        ast = parse(tokens)
        standardized_tree = generate_standardized_tree(ast)
        print("Output of the above program is:")
        get_result(standardized_tree)
        
        