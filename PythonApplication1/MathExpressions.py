from enum import Enum
import MathParser

class Expression():
    def __init__(self, grammar = None):
        self.grammar = grammar
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
    
    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return not self == other

    def find_all(self, type):
        return FindAllVisitor().FindAll(self, type)

    def for_all(self, func):
        return ForAllVisitor().ForAll(self, func)

    def print(self):
        return ''

class Number(Expression):
    def __init__(self, grammar = None):
        return super().__init__(grammar = grammar)

    @staticmethod
    def from_grammar(grammar):
        if isinstance(grammar, MathParser.Integer):
            return Integer.from_grammar(grammar)
        if isinstance(grammar, MathParser.Decimal):
            return Decimal.from_grammar(grammar)

class Integer(Number):
    def __init__(self, value, grammar = None):
        self.value = value
        return super().__init__(grammar = grammar)

    @staticmethod
    def from_grammar(grammar):
        return Integer(grammar.value, grammar = grammar)
    
    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def print(self):
        return str(self.value)

class Decimal(Number):
    def __init__(self, value, grammar = None):
        self.value = value
        return super().__init__(grammar = grammar)

    @staticmethod
    def from_grammar(grammar):
        return Decimal(grammar.value, grammar = grammar)
    
    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def print(self):
        return str(self.value)

class Variable(Expression):
    def __init__(self, name, grammar = None):
        self.name = name
        return super().__init__(grammar = grammar)

    @staticmethod
    def from_grammar(grammar):
        return Variable(grammar.name, grammar = grammar)

    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name

    def print(self):
        return str(self.name)

class Function(Expression):
    def __init__(self, name, body, grammar = None):
        self.name = name
        self.body = body
        return super().__init__(grammar = grammar)

    @staticmethod
    def from_grammar(grammar):
        return Function(grammar.name, Expression.from_grammar(grammar.body), grammar = grammar)
    
    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name and self.body == other.body

    def print(self):
        return self.name + '[' + self.body.print() + ']'

class Unary(Expression):
    def __init__(self, grammar = None):
        return super().__init__(grammar = grammar)

    @staticmethod
    def from_grammar(grammar):
        if isinstance(grammar, MathParser.SingleExpression):
            if grammar.negative:
                return Negation(Expression.from_grammar(grammar.body), grammar = grammar)
            else:
                return Expression.from_grammar(grammar.body)

class Negation(Unary):
    def __init__(self, body, grammar = None):
        self.body = body
        return super().__init__(grammar = grammar)

    def print(self):
        return '-' + self.body.print()
    
    def __eq__(self, other):
        return type(self) == type(other) and self.body == other.body

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
    def __init__(self, method, expressions, grammar = None):
        self.method = method
        self.expressions = expressions
        return super().__init__(grammar = grammar)

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

        return Operation(method, expressions, grammar = grammar)
    
    def __eq__(self, other):
        a = self
        b = other

        # other must also be an Operation
        if not type(a) == type(b):
            return False

        # operations must use the same methods
        if not a.method == b.method:
            return False

        # count of expressions must be the same
        if not len(a.expressions) == len(b.expressions):
            return False

        # check for equality of all expressions
        if not all(i == j for i, j in zip(a.expressions, b.expressions)):
            return False

        return True

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

    def Transform(self, expression):
        if isinstance(expression, Number):
            return self.TransformNumber(expression)
        if isinstance(expression, Variable):
            return self.TransformVariable(expression)
        if isinstance(expression, Function):
            return self.TransformFunction(expression)
        if isinstance(expression, Unary):
            return self.TransformUnary(expression)
        if isinstance(expression, Operation):
            return self.TransformOperation(expression)

    def TransformMany(self, expressions):
        l = []
        for e in expressions:
            l.append(self.Transform(e))
        return l

    def TransformNumber(self, expression):
        if isinstance(expression, Integer):
            return self.TransformInteger(expression)
        if isinstance(expression, Decimal):
            return self.TransformDecimal(expression)

    def TransformInteger(self, expression):
        return Integer(expression.value)

    def TransformDecimal(self, expression):
        return Decimal(expression.value)

    def TransformVariable(self, expression):
        return Variable(expression.name)

    def TransformFunction(self, expression):
        return Function(expression.name, self.Transform(expression.body))

    def TransformUnary(self, expression):
        if isinstance(expression, Negation):
            return self.TransformNegation(expression)

    def TransformNegation(self, expression):
        return Negation(self.Transform(expression.body))

    def TransformOperation(self, expression):
        return Operation(expression.method, self.TransformMany(expression.expressions))

def from_grammar(grammar):
    return Expression.from_grammar(grammar)

def from_grammars(grammars):
    return Expression.from_grammars(grammars)

def parse_text(text):
    return from_grammar(MathParser.parse_text(text))
    
def parse_file(path):
    return from_grammar(MathParser.parse_file(path))

class FindAllVisitor(Visitor):

    def FindAll(self, expression, type):
        self.find = []
        self.type = type
        self.Visit(expression)
        return self.find;

    def Visit(self, expression):
        if isinstance(expression, self.type):
            self.find.append(expression)
        super().Visit(expression)

class ForAllVisitor(Visitor):

    def ForAll(self, expression, func):
        self.func = func
        self.Visit(expression)

    def Visit(self, expression):
        self.func(expression)
        super().Visit(Expression)
