import sys
from modgrammar import *

grammar_whitespace_mode = 'optional'

class Name (Grammar):
    grammar = (WORD('A-Za-z', 'A-Za-z0-9_'))

class Number (Grammar):
    grammar = (WORD('0-9'), OPTIONAL('.', WORD('0-9')))

class ParenExpr (Grammar):
    grammar = (L('('), REF('Expr'), L(')'))

class FuncExpr (Grammar):
    grammar = (Name, L('['), REF('Expr'), L(']'))

class ValueExpr (Grammar):
    grammar = (OPTIONAL('-'), ParenExpr | FuncExpr | Name | Number)

class P0Term (Grammar):
    grammar = (ValueExpr)

class P0Expr (Grammar):
    grammar = (P0Term, ONE_OR_MORE(L('^'), P0Term))

class P1Term (Grammar):
    grammar = (P0Expr | ValueExpr)

class P1Expr (Grammar):
    grammar = (P1Term, ONE_OR_MORE(L('/'), P1Term))

class P2Term (Grammar):
    grammar = (P0Expr | P1Expr | ValueExpr)

class P2Expr (Grammar):
    grammar = (P2Term, ONE_OR_MORE(L('*'), P2Term))

class P3Term (Grammar):
    grammar = (P0Expr | P1Expr | P2Expr | ValueExpr)

class P3Expr (Grammar):
    grammar = (P3Term, ONE_OR_MORE(L('+') | L('-'), P3Term))

class Expr (Grammar):
    grammar = (P3Expr | P2Expr | P1Expr | P0Expr | ValueExpr)

if __name__ == '__main__':
    Expr.grammar_resolve_refs()
    parser = Expr.parser()
    result = parser.parse_text(open('TextFile1.txt', 'r').read(), eof=True)
    remainder = parser.remainder()
    print("Parsed Text: {}".format(result))
    print("Unparsed Text: {}".format(remainder))