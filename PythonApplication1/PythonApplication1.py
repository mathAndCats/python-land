import sys
import MathExpressions
import MathParser

class ReplaceMutiplicationWithDivide(MathExpressions.Transformer):
    def TransformSequence(self, expression):
        if expression.method == MathExpressions.OperationMethod.Multiply:
            return MathExpressions.Sequence(MathExpressions.OperationMethod.Divide, list(self.TransformMany(expression.expressions)))
        else:
            return super().TransformOperation(expression)

if __name__ == '__main__':
    e = MathExpressions.parse_text('-(-a)')
    print(e)
