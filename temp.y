    def parse(self):
        self.parse_E()
        if self.next_token is not None:
            self.error("Extra input after parsing")
        return self.stack[-1]
    
    def parse_E(self):
        if self.peek() == 'let':
            self.read('let')
            self.parse_D()
            self.read('in')
            self.parse_E()
            self.write('let', 2)
        elif self.peek() == 'fn':
            self.read('fn')
            vb_count = 0
            while self.peek().isidentifier():
                self.read(self.peek())
                vb_count += 1
            self.read('.')
            self.parse_E()
            self.write('lambda', vb_count + 1)
        else:
            self.parse_Ew()

    def parse_Ew(self):
        self.parse_T()
        if self.peek() == 'where':
            self.read('where')
            self.parse_Dr()
            self.write('where', 2)

    def parse_T(self):
        self.parse_Ta()
        count = 0
        while self.peek() == ',':
            self.read(',')
            self.parse_Ta()
            count += 1
        if count > 0:
            self.write('tau', count + 1)

    def parse_Ta(self):
        self.parse_Tc()
        while self.peek() == 'aug':
            self.read('aug')
            self.parse_Tc()
            self.write('aug', 2)

    def parse_Tc(self):
        self.parse_B()
        while self.peek() in {'->', '|'}:
            op = self.peek()
            self.read(op)
            self.parse_Tc()
            self.write(op, 2)

    def B(self):
        self.Bt()
        while self.match('or'):
            self.Bt()

    def Bt(self):
        self.Bs()
        while self.match('&'):
            self.Bs()

    def Bs(self):
        if self.match('not'):
            self.Bp()
        else:
            self.Bp()

    def Bp(self):
        self.A()
        if self.match('gr') or self.match('>'):
            self.A()
        elif self.match('ge') or self.match('>='):
            self.A()
        elif self.match('ls') or self.match('<'):
            self.A()
        elif self.match('le') or self.match('<='):
            self.A()
        elif self.match('eq'):
            self.A()
        elif self.match('ne'):
            self.A()

    #############################
    # Arithmetic Expressions
    #############################

    def A(self):
        self.At()
        while self.match('+') or self.match('-'):
            self.At()

    def At(self):
        if self.match('-'):
            self.At()  # Unary negation
        else:
            self.Af()
            while self.match('*') or self.match('/'):
                self.Af()

    def Af(self):
        self.Ap()
        if self.match('**'):
            self.Af()

    def Ap(self):
        self.primary()
        while self.match('@'):
            self.expect('<IDENTIFIER>')
            self.R()

    #############################
    # Rators and Rands
    #############################

    def R(self):
        if self.match('gamma'):
            self.Rn()

    def Rn(self):
        if self.match('<IDENTIFIER>') or self.match('<INTEGER>') or self.match('<STRING>'):
            return
        elif self.match('true') or self.match('false') or self.match('nil'):
            return
        elif self.match('('):
            self.E()
            self.expect(')')
        elif self.match('dummy'):
            return
        else:
            raise SyntaxError("Invalid Rn")

    #############################
    # Definitions
    #############################

    def D(self):
        self.Da()
        if self.match('within'):
            self.D()

    def Da(self):
        self.Dr()
        while self.match('and'):
            self.Dr()

    def Dr(self):
        if self.match('rec'):
            self.Db()
        else:
            self.Db()

    def Db(self):
        if self.match('('):
            self.D()
            self.expect(')')
        else:
            self.expect('<IDENTIFIER>')
            self.Vb()
            self.expect('=')
            self.E()

    #############################
    # Variables
    #############################

    def Vb(self):
        if self.match('<IDENTIFIER>'):
            return
        elif self.match('('):
            if self.current_token != ')':
                self.Vl()
            self.expect(')')

    def Vl(self):
        self.expect('<IDENTIFIER>')
        while self.match(','):
            self.expect('<IDENTIFIER>')

    #############################
    # General Entry Point
    #############################

    def E(self):
        # E could be A or B depending on context
        # You may need to separate if required
        self.B()
