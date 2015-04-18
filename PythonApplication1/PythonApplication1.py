import sys
from modgrammar import *

grammar_whitespace_mode = 'optional'

class Name (Grammar):
    grammar = (WORD('A-Za-z', 'A-Za-z0-9_'))

    def print(self):
        return self[0];

class Number (Grammar):
    grammar = (WORD('0-9'))

    def print(self):
        return self[0];

class ParenExpr (Grammar):
    grammar = (L('('), REF('Expr'), L(')'))

    def print(self):
        return '(' + self[1] + ')'

class FuncExpr (Grammar):
    grammar = (Name, L('['), REF('Expr'), L(']'))

    def grammar_elem_init(self, sessiondata):
        self.name = self[0].string
        self.expr = self[2]

    def print(self):
        return self.name + '[' + self.expr.print() + ']'

class ValueExpr (Grammar):
    grammar = (OPTIONAL('-'), ParenExpr | FuncExpr | Name | Number)

    def print(self):
        negative = self[0] and self[0].string == '-'
        if (negative):
            return '-' + self[1].print();
        else:
            return self[0].print()

class P0Term (Grammar):
    grammar = (ValueExpr)

    def print(self):
        return self[0].print()

class P0Expr (Grammar):
    grammar = (P0Term, ONE_OR_MORE(L('^'), P0Term))

    def print(self):
        return self[0].print() + '^' + self[2].print()


class P1Term (Grammar):
    grammar = (P0Expr | ValueExpr)

    def print(self):
        return self[0].print()

class P1Expr (Grammar):
    grammar = (P1Term, ONE_OR_MORE(L('/'), P1Term))

    def print(self):
        value = self[0].print()
        for e in self[1]:
            value += e[0].string
            value += e[1].print()
        return value;

class P2Term (Grammar):
    grammar = (P0Expr | P1Expr | ValueExpr)

    def print(self):
        return self[0].print()

class P2Expr (Grammar):
    grammar = (P2Term, ONE_OR_MORE(L('*'), P2Term))

    def string(self):
        value = self[0].print()
        for e in self[1]:
            value += e[0].string
            value += e[1].print()
        return value;

class P3Term (Grammar):
    grammar = (P0Expr | P1Expr | P2Expr | ValueExpr)

    def print(self):
        return self[0].print()

class P3Expr (Grammar):
    grammar = (P3Term, ONE_OR_MORE(L('+') | L('-'), P3Term))

    def print(self):
        value = self[0].print()
        for e in self[1]:
            value += e[0].string
            value += e[1].print()
        return value;

class Expr (Grammar):
    grammar = (P3Expr | P2Expr | P1Expr | P0Expr | ValueExpr)

    def print(self):
        return self[0].print()

if __name__ == '__main__':
    parser = Expr.parser()
    with open('TextFile1.txt', 'r') as t:
        file = t.read()
        result = parser.parse_text(file, eof = True)
        print(result.print())
    
