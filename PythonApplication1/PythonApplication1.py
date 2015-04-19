import sys
import MathExpressions

class ReplaceMutiplicationWithDivide(MathExpressions.Transformer):
    def TransformOperation(self, expression):
        if expression.method == MathExpressions.OperationMethod.Multiply:
            return MathExpressions.Operation(MathExpressions.OperationMethod.Divide, list(self.TransformMany(expression.expressions)))
        else:
            return super().TransformOperation(expression)

if __name__ == '__main__':
    e = MathExpressions.parse_file('TextFile1.txt')
    print(e)
    
    #e2 = ReplaceMutiplicationWithDivide().Transform(e)
    #print(e2)

    find = MathExpressions.parse_text('DiracDelta[w + omega_p + omega_r + 2 * omega_y]')

    for f in e.find_all(MathExpressions.Function):
        if f == find:
            print(f)
