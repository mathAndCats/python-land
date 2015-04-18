import sys
from modgrammar import *

grammar_whitespace_mode = 'optional'

class BaseGrammar (Grammar):

    def print(self):
        return ''

class Identifier (BaseGrammar):
    grammar = (WORD('A-Za-z', 'A-Za-z0-9_'))

    def grammar_elem_init(self, sessiondata):
        self.id = self[0].string

    def print(self):
        return self.id

class Number (BaseGrammar):
    grammar = (WORD('0-9'))

    def grammar_elem_init(self, sessiondata):
        self.value = float(self[0].string)

    def print(self):
        return str(self.value)

class Variable (BaseGrammar):
    grammar = (Identifier,)

    def grammar_elem_init(self, sessiondata):
        self.name = self[0].id

    def print(self):
        return self.name

class Paren (BaseGrammar):
    grammar = (L('('), REF('Expr'), L(')'))

    def grammar_elem_init(self, sessiondata):
        self.body = self[1]

    def print(self):
        return '(' + self.body.print() + ')'

class Func (BaseGrammar):
    grammar = (Identifier, L('['), REF('Expr'), L(']'))

    def grammar_elem_init(self, sessiondata):
        self.name = self[0].id
        self.body = self[2]

    def print(self):
        return self.name + '[' + self.body.print() + ']'

class Value (BaseGrammar):
    grammar = (OPTIONAL('-'), Paren | Func | Variable | Number)

    def grammar_elem_init(self, sessiondata):
        self.negative = self[0] and self[0].string == '-'
        self.body = self[1]

    def print(self):
        return self.body.print()

class Operation (BaseGrammar):

    def grammar_elem_init(self, sessiondata):
        self.expressions = [self[0]]
        for e in self[1]:
            self.expressions.append(e[0])
            self.expressions.append(e[1])

    def print(self):
        value = ''
        for e in self.expressions:
            if e.print:
                value += e.print()
            else:
                value += e.string
        return value;


class P0Term (BaseGrammar):
    grammar = (Value,)
    grammar_collapse = True

class P0Expr (Operation):
    grammar = (P0Term, ONE_OR_MORE(L('^'), P0Term))

class P1Term (BaseGrammar):
    grammar = (P0Expr | Value)
    grammar_collapse = True

class P1Expr (Operation):
    grammar = (P1Term, ONE_OR_MORE(L('/'), P1Term))

class P2Term (BaseGrammar):
    grammar = (P0Expr | P1Expr | Value)
    grammar_collapse = True

class P2Expr (Operation):
    grammar = (P2Term, ONE_OR_MORE(L('*'), P2Term))

class P3Term (BaseGrammar):
    grammar = (P0Expr | P1Expr | P2Expr | Value)
    grammar_collapse = True

class P3Expr (Operation):
    grammar = (P3Term, ONE_OR_MORE(L('+') | L('-'), P3Term))

class Expr (BaseGrammar):
    grammar = (P3Expr | P2Expr | P1Expr | P0Expr | Value)
    grammar_collapse = True

    def print(self):
        return self[0].print()

if __name__ == '__main__':
    parser = Expr.parser()
    with open('TextFile1.txt', 'r') as t:
        file = t.read()
        result = parser.parse_text(file, eof = True)
        print(result.print())

        for e in result.find_all(Func):
            if e.name == 'DiracDelta':
                print(e.print())
    
