import sys
import MathExpressions

class ReplaceMutiplicationWithDivide(MathExpressions.Transformer):

    def VisitOperation(self, expression):
        if expression.method == MathExpressions.OperationMethod.Multiply:
            return MathExpressions.Operation(MathExpressions.OperationMethod.Divide, self.VisitMany(expression.expressions))
        else:
            return super().VisitOperation(expression)

if __name__ == '__main__':
    e = MathExpressions.parse_file('TextFile1.txt')
    print(e.print())
    
    e2 = ReplaceMutiplicationWithDivide().Visit(e)
    print(e2.print())