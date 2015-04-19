from enum import Enum
import MathParser

class GrammarParseException(Exception):
    pass

class Expression():
    def __init__(self, grammar = None):
        self.grammar = grammar
        self.parent = None
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
            return Sequence.from_grammar(grammar)
        if isinstance(grammar, MathParser.SingleExpression):
            return Unary.from_grammar(grammar)
        if isinstance(grammar, MathParser.Paren):
            return Expression.from_grammar_paren(grammar)

        raise GrammarParseException(str(grammar))

    @staticmethod
    def from_grammar_paren(grammar):
            return Expression.from_grammar(grammar.body)

    @staticmethod
    def from_grammars(grammars):
        for e in grammars:
            yield Expression.from_grammar(e)
    
    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return 'EXPRESSION'

    def __repr__(self):
        return str(self)

    def find_all(self, type = None, func = None):
        return FindAllVisitor().FindAll(self, type = type, func = func)

    def for_all(self, func):
        return ForAllVisitor().ForAll(self, func)

class Number(Expression):
    def __init__(self, grammar = None):
        super().__init__(grammar = grammar)

    @staticmethod
    def from_grammar(grammar):
        if isinstance(grammar, MathParser.Integer):
            return Integer.from_grammar(grammar)
        if isinstance(grammar, MathParser.Decimal):
            return Decimal.from_grammar(grammar)

class Integer(Number):
    def __init__(self, value, grammar = None):
        super().__init__(grammar = grammar)
        self.value = value

    @staticmethod
    def from_grammar(grammar):
        return Integer(grammar.value, grammar = grammar)
    
    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def __str__(self):
        return str(self.value)

class Decimal(Number):
    def __init__(self, value, grammar = None):
        super().__init__(grammar = grammar)
        self.value = value

    @staticmethod
    def from_grammar(grammar):
        return Decimal(grammar.value, grammar = grammar)
    
    def __eq__(self, other):
        return type(self) == type(other) and self.value == other.value

    def __str__(self):
        return str(self.value)

class Variable(Expression):
    def __init__(self, name, grammar = None):
        super().__init__(grammar = grammar)
        self.name = name

    @staticmethod
    def from_grammar(grammar):
        return Variable(grammar.name, grammar = grammar)

    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name

    def __str__(self):
        return str(self.name)

class Function(Expression):
    def __init__(self, name, body, grammar = None):
        super().__init__(grammar = grammar)
        self.name = name
        self.body = body
        self.body.parent = self

    @staticmethod
    def from_grammar(grammar):
        return Function(grammar.name, Expression.from_grammar(grammar.body), grammar = grammar)
    
    def __eq__(self, other):
        return type(self) == type(other) and self.name == other.name and self.body == other.body

    def __str__(self):
        return self.name + '[' + str(self.body) + ']'

class Unary(Expression):
    def __init__(self, grammar = None):
        super().__init__(grammar = grammar)

    @staticmethod
    def from_grammar(grammar):
        if isinstance(grammar, MathParser.SingleExpression):
            if grammar.negative:
                return Negation(Expression.from_grammar(grammar.body), grammar = grammar)
            else:
                return Expression.from_grammar(grammar.body)

class Negation(Unary):
    def __init__(self, body, grammar = None):
        super().__init__(grammar = grammar)
        self.body = body
        self.body.parent = self

    def __str__(self):
        if isinstance(self.body, Negation):
            return '-' + '(' + str(self.body) + ')'
        if isinstance(self.body, Sequence):
            return '-' + '(' + str(self.body) + ')'
        else:
            return '-' + str(self.body)
    
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

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

class Operation(Expression):
    def __init__(self, method, operand, grammar = None):
        super().__init__(grammar = grammar)
        self.method = method
        self.operand = operand
        self.operand.parent = self

    def __eq__(self, other):
        return type(self) == type(other) and self.method == other.method and self.operand == other.operand

    def __str__(self):
        if self.method != None:
            if isinstance(self.operand, Sequence) and len(self.operand.operations) > 1:
                return ' ' + str(self.method) + ' ' + '(' + str(self.operand) + ')'
            else:
                return ' ' + str(self.method) + ' ' + str(self.operand)
        else:
            if isinstance(self.operand, Sequence) and len(self.operand.operations) > 1:
                return '(' + str(self.operand) + ')'
            else:
                return str(self.operand)

class Sequence(Expression):
    def __init__(self, operations, grammar = None):
        super().__init__(grammar = grammar)
        self.operations = list(operations)

        for e in self.operations:
            e.parent = self

    @staticmethod
    def from_grammar(grammar):

        # assemble underlying sequence of grammar parts, with a prepended None operation
        grammar_expressions = list(grammar.expressions)
        grammar_expressions.insert(0, None)

        operations = []

        for i in range(0, len(grammar_expressions), 2):
            oper = grammar_expressions[i]
            expr = grammar_expressions[i + 1]
            
            # generate method and expression
            method = OperationMethod.from_grammar(oper) if oper != None else None
            expression = Expression.from_grammar(expr)

            # create new operation
            operand = Operation(method, expression, oper if oper != None else expr)
            operations.append(operand)

        return Sequence(operations, grammar = grammar)
    
    def __eq__(self, other):
        a = self
        b = other

        # other must also be an Sequence
        if not type(a) == type(b):
            return False

        # count of operations must be the same
        if not len(a.operations) == len(b.operations):
            return False

        # check for equality of all operations
        if not all(i == j for i, j in zip(a.operations, b.operations)):
            return False

        return True

    def __str__(self):
        return ''.join(map(lambda x : str(x), self.operations))

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
        if isinstance(expression, Sequence):
            self.VisitSequence(expression)
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
        pass

    def VisitDecimal(self, expression):
        pass

    def VisitVariable(self, expression):
        pass

    def VisitFunction(self, expression):
        self.Visit(expression.body)

    def VisitUnary(self, expression):
        if isinstance(expression, Negation):
            self.VisitNegation(expression)

    def VisitNegation(self, expression):
        self.Visit(expression.body)

    def VisitSequence(self, expresion):
        self.VisitMany(expresion.operations)

    def VisitOperation(self, operation):
        pass

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
        if isinstance(expression, Sequence):
            return self.TransformSequence(expression)
        if isinstance(expression, Operation):
            return self.TransformOperation(expression)

    def TransformMany(self, expressions):
        for e in expressions:
             yield self.Transform(e)

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

    def TransformSequence(self, expression):
        return Sequence(self.TransformMany(expression.operations))

    def TransformOperation(self, expression):
        return Operation(expression.method, self.Transform(expression.operand))

def from_grammar(grammar):
    return Expression.from_grammar(grammar)

def from_grammars(grammars):
    return Expression.from_grammars(grammars)

def parse_text(text):
    return from_grammar(MathParser.parse_text(text))
    
def parse_file(path):
    return from_grammar(MathParser.parse_file(path))

class FindAllVisitor(Visitor):

    def FindAll(self, expression, type = Expression, func = None):
        self.find = []
        self.type = type
        self.func = func
        self.Visit(expression)
        return self.find;

    def Visit(self, expression):
        if self.type == None or isinstance(expression, self.type):
            if self.func == None or self.func(expression):
                self.find.append(expression)
        super().Visit(expression)

class ForAllVisitor(Visitor):

    def ForAll(self, expression, func):
        self.func = func
        self.Visit(expression)

    def Visit(self, expression):
        self.func(expression)
        super().Visit(Expression)
