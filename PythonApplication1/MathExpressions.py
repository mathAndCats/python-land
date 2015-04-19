from enum import Enum
import MathParser

class Expression():
    def __init__(self):
        return super().__init__()
    
    @staticmethod
    def from_grammar(grammar):
        if isinstance(grammar, MathParser.Variable):
            return Variable.from_grammar(grammar)
        if isinstance(grammar, MathParser.Number):
            return Number.from_grammar(grammar)
        if isinstance(grammar, MathParser.Func):
            return Function.from_grammar(grammar)
        if isinstance(grammar, MathParser.MathExpression):
            return Operation.from_grammar(grammar)
        if isinstance(grammar, MathParser.SingleExpression):
            return Expression.from_grammar_single(grammar)
        if isinstance(grammar, MathParser.Paren):
            return Expression.from_grammar_paren(grammar)

        print(type(grammar))

    @staticmethod
    def from_grammar_single(grammar):
        if grammar.negative:
            return Negation(Expression.from_grammar(grammar.body))
        else:
            return Expression.from_grammar(grammar.body)

    @staticmethod
    def from_grammar_paren(grammar):
            return Expression.from_grammar(grammar.body)

    @staticmethod
    def from_grammars(grammars):
        l = []
        for e in grammars:
            l.append(Expression.from_grammar(e))
        return l

    def print(self):
        return ''

class Number(Expression):
    def __init__(self):
        return super().__init__()

    @staticmethod
    def from_grammar(grammar):
        if isinstance(grammar, MathParser.Integer):
            return Integer.from_grammar(grammar)
        if isinstance(grammar, MathParser.Decimal):
            return Decimal.from_grammar(grammar)

class Integer(Number):
    def __init__(self, value):
        self.value = value
        return super().__init__()

    @staticmethod
    def from_grammar(grammar):
        return Decimal(grammar.value)

    def print(self):
        return str(self.value);

class Decimal(Number):
    def __init__(self, value):
        self.value = value
        return super().__init__()

    @staticmethod
    def from_grammar(grammar):
        return Decimal(grammar.value)

    def print(self):
        return str(self.value);

class Variable(Expression):
    def __init__(self, name):
        self.name = name
        return super().__init__()

    @staticmethod
    def from_grammar(grammar):
        return Variable(grammar.name)

    def print(self):
        return str(self.name);

class Function(Expression):
    def __init__(self, name, body):
        self.name = name
        self.body = body
        return super().__init__()

    @staticmethod
    def from_grammar(grammar):
        return Function(grammar.name, Expression.from_grammar(grammar.body))

    def print(self):
        return self.name + '[' + self.body.print() + ']'

class Negation(Expression):
    def __init__(self, body):
        self.body = body
        return super().__init__()

    def print(self):
        return '-' + self.body.print()

class OperationMethod(Enum):
    Power = '^'
    Divide = '/'
    Multiply = '*'
    Add = '+'
    Subtract = '-'
    
    @staticmethod
    def from_grammar(expr):
        if expr.string == '+':
            return OperationMethod.Add
        if expr.string == '-':
            return OperationMethod.Subtract
        if expr.string == '*':
            return OperationMethod.Multiply
        if expr.string == '/':
            return OperationMethod.Divide
        if expr.string == '^':
            return OperationMethod.Power

    def print(self):
        return self.value

class Operation(Expression):
    def __init__(self, method, expressions):
        self.method = method
        self.expressions = expressions
        return super().__init__()

    @staticmethod
    def from_grammar(grammar):
        method = None
        expressions = []
        for i in range(0, len(grammar.expressions)):
            expr = grammar.expressions[i]
            if i % 2 == 0:
                expressions.append(Expression.from_grammar(expr))
            elif method == None:
                method = OperationMethod.from_grammar(expr)

        return Operation(method, expressions)

    def print(self):
        values = []
        for e in self.expressions:
            values.append(e.print())
        return '(' + self.method.print().join(values) + ')'


def from_grammar(grammar):
    return Expression.from_grammar(grammar)

def from_grammars(grammars):
    return Expression.from_grammars(grammars)
