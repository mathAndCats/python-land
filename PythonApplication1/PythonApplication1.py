import sys
import MathExpressions

if __name__ == '__main__':
    e = MathExpressions.parse_file('TextFile1.txt')
    print(e.print())
    
    e2 = MathExpressions.Transformer().Visit(e)
    print(e2.print())