class Scanner:
    current_token = ''
    current_state = ''
    tokens = []
    valid_operators = ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$', 
                   '!', '#', '%', '^', '_', '[', ']', '{', '}', '"', "'", '?']

    def state_identifier(self, remaining_input):
        self.current_state = 'IDENTIFIER'
        self.current_token += remaining_input[0]
        
        i = 1 
        while i < len(remaining_input) and (remaining_input[i].isalnum() or remaining_input[i] == '_'):
            self.current_token += remaining_input[i]
            i += 1

        if i >= len(remaining_input):
            self.state_start('')
            return
        
        if remaining_input[i] in [' ','\t','\n']:
            self.state_start(remaining_input[i+1:])
            return
            # close bracket can be eliminated
        elif remaining_input[i] in self.valid_operators + ['(', ')', ';', ',']:
            self.state_start(remaining_input[i:])    
            return
        else:
            self.state_unknown(remaining_input[i:])
            return

    def state_integer(self, remaining_input):
        self.current_state = 'INTEGER'
        self.current_token += remaining_input[0]
        
        i = 1 
        while i < len(remaining_input) and remaining_input[i].isdigit():
            self.current_token += remaining_input[i]
            i += 1
        
        if i >= len(remaining_input):
            self.state_start('')
            return
        
        if remaining_input[i] in [' ','\t','\n']:
            self.state_start(remaining_input[i+1:])
            return
        elif remaining_input[i] in self.valid_operators + ['(', ')', ';', ',']:
            self.state_start(remaining_input[i:])
            return
        else:
            self.state_unknown(remaining_input[i:])
            return

    # Try to impleent using finite state machine
    def state_Operator(self, remaining_input):
        self.current_state = 'OPERATOR'
        
        self.current_token += remaining_input[0]
        
        i = 1 
        while i < len(remaining_input) and remaining_input[i] in self.valid_operators:
            self.current_token += remaining_input[i]
            i += 1

        if i >= len(remaining_input):
            self.state_start('')
            return
        
        if remaining_input[i] in [' ','\t','\n']:
            if self.current_token == '//':
                self.state_comment(remaining_input[i:])
                return
            else:
                self.current_state = 'OPERATOR'
            self.state_start(remaining_input[i+1:])
            return
        else:
            self.state_start(remaining_input[i:])
            return

    def state_string(self, remaining_input):
        self.current_state = 'STRING'

        self.current_token += remaining_input[0]
        
        i = 1 
        # To do : check the case /''
        while i < len(remaining_input) and not (remaining_input[i:i+2] == "''" and remaining_input[i-1] == "\\"):
            self.current_token += remaining_input[i]
            i += 1

        if i >= len(remaining_input):
            self.state_start('')
            return
        
        if remaining_input[i] in [' ','\t','\n']:
            self.state_start(remaining_input[i+1:])
            return
        elif remaining_input[i] in self.valid_operators+ ['(', ')', ';', ',']:
            self.state_start(remaining_input[i:])
            return
        else:
            self.state_unknown(remaining_input[i:])
            return

    def state_comment(self, remaining_input):
        self.current_state = 'COMMENT'
        self.current_token += remaining_input[0]
        
        i = 1 
        while i < len(remaining_input) and remaining_input[i] != '\n':
            i += 1
        
        if i >= len(remaining_input):
            self.state_start('')
            return
        
        self.state_start(remaining_input[i:])
        return
    
    def state_unknown(self, remaining_input):
        self.current_state = 'UNKNOWN'
        i = 1 
        while i < len(remaining_input) and not (remaining_input[i] in [' ','\t','\n']):
            self.current_token += remaining_input[i]
            i += 1

        if i >= len(remaining_input):
            self.state_start('')
            return
        
        if remaining_input[i] in [' ','\t','\n']:
            self.state_start(remaining_input[i+1:])
            return
        else:
            self.state_unknown(remaining_input[i:])
            return

    def state_open_bracket(self, remaining_input):
        self.current_state = 'OPEN_BRACKET'
        self.current_token += remaining_input[0]
        self.state_start(remaining_input[1:])
        return
       
    def state_close_bracket(self, remaining_input):
        self.current_state = 'CLOSE_BRACKET'
        self.current_token += remaining_input[0]
        self.state_start(remaining_input[1:])
        return

    def state_semicolon(self, remaining_input):
        self.current_state = 'SEMICOLON'
        self.current_token += remaining_input[0]
        self.state_start(remaining_input[1:])
        return

    def state_comma(self, remaining_input):
        self.current_state = 'COMMA'
        self.current_token += remaining_input[0]
        self.state_start(remaining_input[1:])
        return

    def state_start(self, remaining_input):

        self.tokens.append((self.current_state, self.current_token))
        self.current_token = ''
        self.current_state = ''

        while remaining_input != '':
            if remaining_input[0].isalpha():
                self.state_identifier(remaining_input)
                return
            elif remaining_input[0].isdigit():
                self.state_integer(remaining_input)
                return
            elif remaining_input[0] in ['+', '-', '*', '<', '>', '&', '.', '@', '/', ':', '=', '~', '|', '$', 
                        '!', '#', '%', '^', '_', '[', ']', '{', '}', '"', "'", '?']:
                self.state_Operator(remaining_input)
                return
            elif remaining_input[0] == "'":
                self.state_string(remaining_input)
                return
            elif remaining_input[0] == '/':
                self.state_comment(remaining_input)
                return
            elif remaining_input[0] == '(':
                self.state_open_bracket(remaining_input)
                return
            elif remaining_input[0] == ')':
                self.state_close_bracket(remaining_input)
                return
            elif remaining_input[0] == ';':
                self.state_semicolon(remaining_input)
                return
            elif remaining_input[0] == ',':
                self.state_comma(remaining_input)
                return
            elif remaining_input[0] in [' ', '\t', '\n']:
                remaining_input = remaining_input[1:]
                continue
            else:
                self.state_unknown(remaining_input)
                return
    
if __name__ == '__main__':
    scanner = Scanner()
    input_string = """ int main() { return 145+123-523/123; } // This is a comment"""
    scanner.state_start(input_string)
    for token in scanner.tokens:
        print(token)
