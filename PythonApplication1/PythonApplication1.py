import sys
import MathExpressions

class ReplaceMutiplicationWithDivide(MathExpressions.Transformer):

    def TransformOperation(self, expression):
        if expression.method == MathExpressions.OperationMethod.Multiply:
            return MathExpressions.Operation(MathExpressions.OperationMethod.Divide, self.TransformMany(expression.expressions))
        else:
            return super().TransformOperation(expression)

if __name__ == '__main__':
    e = MathExpressions.parse_file('TextFile1.txt')
    print(e.print())
    
    e2 = ReplaceMutiplicationWithDivide().Transform(e)
    print(e2.print())