import sys
import MathParser

if __name__ == '__main__':
    result = MathParser.parse_file('TextFile1.txt')
    print(result.print())

    for e in result.find_all(MathParser.Func):
        if e.name == 'DiracDelta':
            print(e.print())
    
