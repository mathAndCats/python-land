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
    
    def print(self):
        return str(self.value)

class Integer (Number):
    grammar = (WORD('0-9'))

    def grammar_elem_init(self, sessiondata):
        self.value = int(self[0].string)

class Decimal (Number):
    grammar = (WORD('0-9'), L('.'), WORD('0-9'))

    def grammar_elem_init(self, sessiondata):
        self.value = float(self[0].string)

class NumberExpression (BaseGrammar):
    grammar = (Decimal | Integer)
    grammar_collapse = True

class Variable (BaseGrammar):
    grammar = (Identifier,)

    def grammar_elem_init(self, sessiondata):
        self.name = self[0].id

    def print(self):
        return self.name

class Paren (BaseGrammar):
    grammar = (L('('), REF('Expression'), L(')'))

    def grammar_elem_init(self, sessiondata):
        self.body = self[1]

    def print(self):
        return '(' + self.body.print() + ')'

class Func (BaseGrammar):
    grammar = (Identifier, L('['), REF('Expression'), L(']'))

    def grammar_elem_init(self, sessiondata):
        self.name = self[0].id
        self.body = self[2]

    def print(self):
        return self.name + '[' + self.body.print() + ']'

class SingleExpression (BaseGrammar):
    grammar = (OPTIONAL('-'), Paren | Func | Variable | NumberExpression)

    def get_body(self):
        body = self[1]

        if isinstance(body, Paren):
            if isinstance(body.body, SingleExpression):
                if isinstance(body.body.body, Number):
                    return body.body.body
                if isinstance(body.body.body, Variable):
                    return body.body.body
                if isinstance(body.body.body, Paren):
                    return body.body.body
                if isinstance(body.body.body, Func):
                    return body.body.body

        return body

    def grammar_elem_init(self, sessiondata):
        self.negative = self[0] and self[0].string == '-'
        self.body = self.get_body()

    def print(self):
        if self.negative:
            return '-' + self.body.print()
        else:
            return self.body.print()

class MathExpression (BaseGrammar):

    def grammar_elem_init(self, sessiondata):
        self.expressions = [self[0]]
        for e in self[1]:
            self.expressions.append(e[0])
            self.expressions.append(e[1])

    def print(self):
        values = []
        for e in self.expressions:
            if isinstance(e, BaseGrammar):
                values.append(e.print())
            else:
                values.append(e.string)
        return ' '.join(values)


class P0OperationTerm (BaseGrammar):
    grammar = (SingleExpression,)
    grammar_collapse = True

class P0OperationExpression (MathExpression):
    grammar = (P0OperationTerm, ONE_OR_MORE(L('^'), P0OperationTerm))

class P1OperationTerm (BaseGrammar):
    grammar = (P0OperationExpression | SingleExpression)
    grammar_collapse = True

class P1OperationExpression (MathExpression):
    grammar = (P1OperationTerm, ONE_OR_MORE(L('/'), P1OperationTerm))

class P2OperationTerm (BaseGrammar):
    grammar = (P0OperationExpression | P1OperationExpression | SingleExpression)
    grammar_collapse = True

class P2OperationExpression (MathExpression):
    grammar = (P2OperationTerm, ONE_OR_MORE(L('*'), P2OperationTerm))

class P3OperationTerm (BaseGrammar):
    grammar = (P0OperationExpression | P1OperationExpression | P2OperationExpression | SingleExpression)
    grammar_collapse = True

class P3OperationExpression (MathExpression):
    grammar = (P3OperationTerm, ONE_OR_MORE(L('+') | L('-'), P3OperationTerm))

class Expression (BaseGrammar):
    grammar = (P3OperationExpression | P2OperationExpression | P1OperationExpression | P0OperationExpression | SingleExpression)
    grammar_collapse = True

if __name__ == '__main__':
    Expression.grammar_resolve_refs()
    parser = Expression.parser()
    with open('TextFile1.txt', 'r') as t:
        file = t.read()
        result = parser.parse_text(file, eof = True)
        print(result.print())

        for e in result.find_all(Func):
            if e.name == 'DiracDelta':
                print(e.print())
    
