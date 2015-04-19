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
            return Unary.from_grammar(grammar)
        if isinstance(grammar, MathParser.Paren):
            return Expression.from_grammar_paren(grammar)

        print(type(grammar))

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
        return str(self.value)

class Decimal(Number):
    def __init__(self, value):
        self.value = value
        return super().__init__()

    @staticmethod
    def from_grammar(grammar):
        return Decimal(grammar.value)

    def print(self):
        return str(self.value)

class Variable(Expression):
    def __init__(self, name):
        self.name = name
        return super().__init__()

    @staticmethod
    def from_grammar(grammar):
        return Variable(grammar.name)

    def print(self):
        return str(self.name)

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

class Unary(Expression):
    def __init__(self):
        return super().__init__()

    @staticmethod
    def from_grammar(grammar):
        if isinstance(grammar, MathParser.SingleExpression):
            if grammar.negative:
                return Negation(Expression.from_grammar(grammar.body))
            else:
                return Expression.from_grammar(grammar.body)

class Negation(Unary):
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

    def priority(self):
        if self.value == '^':
            return 5
        if self.value == '/':
            return 4
        if self.value == '*':
            return 3
        if self.value == '+':
            return 2
        if self.value == '-':
            return 2

    def print(self):
        if self.value == '^':
            return self.value
        else:
            return ' ' + self.value + ' '

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
            if isinstance(e, Operation) and self.method.priority() > e.method.priority():
                values.append('(' + e.print() + ')')
            else:
                values.append(e.print())
        return self.method.print().join(values)

class Visitor:

    def Visit(self, expression):
        if isinstance(expression, Number):
            self.VisitNumber(expression)
        if isinstance(expression, Variable):
            self.VisitVariable(expression)
        if isinstance(expression, Function):
            self.VisitFunction(expression)
        if isinstance(expression, Unary):
            self.VisitUnary(expression)
        if isinstance(expression, Operation):
            self.VisitOperation(expression)

    def VisitMany(self, expressions):
        for e in expressions:
            self.Visit(e)

    def VisitNumber(self, expression):
        if isinstance(expression, Integer):
            self.VisitInteger(expression)
        if isinstance(expression, Decimal):
            self.VisitDecimal(expression)

    def VisitInteger(self, expression):
        return

    def VisitDecimal(self, expression):
        return

    def VisitVariable(self, expression):
        return

    def VisitFunction(self, expression):
        self.Visit(expression.body)

    def VisitUnary(self, expression):
        if isinstance(expression, Negation):
            self.VisitNegation(expression)

    def VisitNegation(self, expression):
        self.Visit(expression.body)

    def VisitOperation(self, expresion):
        self.VisitMany(expresion.expressions)

class Transformer:

    def Visit(self, expression):
        if isinstance(expression, Number):
            return self.VisitNumber(expression)
        if isinstance(expression, Variable):
            return self.VisitVariable(expression)
        if isinstance(expression, Function):
            return self.VisitFunction(expression)
        if isinstance(expression, Unary):
            return self.VisitUnary(expression)
        if isinstance(expression, Operation):
            return self.VisitOperation(expression)

    def VisitMany(self, expressions):
        l = []
        for e in expressions:
            l.append(self.Visit(e))
        return l

    def VisitNumber(self, expression):
        if isinstance(expression, Integer):
            return self.VisitInteger(expression)
        if isinstance(expression, Decimal):
            return self.VisitDecimal(expression)

    def VisitInteger(self, expression):
        return Integer(expression.value)

    def VisitDecimal(self, expression):
        return Decimal(expression.value)

    def VisitVariable(self, expression):
        return Variable(expression.name)

    def VisitFunction(self, expression):
        return Function(expression.name, self.Visit(expression.body))

    def VisitUnary(self, expression):
        if isinstance(expression, Negation):
            return self.VisitNegation(expression)

    def VisitNegation(self, expression):
        return Negation(self.Visit(expression.body))

    def VisitOperation(self, expression):
        return Operation(expression.method, self.VisitMany(expression.expressions))

def from_grammar(grammar):
    return Expression.from_grammar(grammar)

def from_grammars(grammars):
    return Expression.from_grammars(grammars)

def parse_text(text):
    return from_grammar(MathParser.parse_text(text))
    
def parse_file(path):
    return from_grammar(MathParser.parse_file(path))
