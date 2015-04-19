import sys
import MathParser
import MathExpressions

if __name__ == '__main__':
    result = MathParser.parse_file('TextFile1.txt')
    print(result.print())

    e = MathExpressions.from_grammar(result)
    print(e.print())
    
