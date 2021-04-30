from collections import namedtuple as NT
from collections import defaultdict
import re
import sys


def make_lexer(rules):
    pats = [(tt, re.compile(pat)) for tt, pat in rules]

    def lex(s):
        while len(s) > 0:
            tt0, v0 = None, None
            for tt, pat in pats:
                m = pat.match(s)
                if m is None:
                    continue
                v = m.group(0)
                # strictly less is important here
                if v0 is None or len(v0) < len(v):
                    tt0, v0 = tt, v
            if tt0 is None:
                raise Exception("lexer got stuck: " + repr(s))
            s = s[len(v0) :]
            if tt0 != "<skip>":
                if tt0 == "<self>":
                    tt0 = v0
                print("lex", tt0, v0)
                yield tt0, v0

    return lex


def make_parser(rules):
    def one_rule(lhs, rhses):
        def one_rhs(tok0, rhs):
            tok = tok0
            ast = [lhs]
            nts = []
            for i, term in enumerate(rhs):
                if len(tok) == 0:
                    return tok0, None
                if term in g.keys():
                    tok, v = g[term](tok)
                    if v is None:
                        return tok0, None
                    nts.append(v)
                else:
                    tt, v = tok[0]
                    tok = tok[1:]
                    if tt != term:
                        return tok0, None
                ast.append(v)
            if len(nts) == 1:
                return tok, nts[0]
            return tok, ast

        def parse(tok0):
            for rhs in rhses:
                tok, ast = one_rhs(tok0, rhs)
                if ast is not None:
                    print("parse", lhs, " ".join(v for tt, v in tok0))
                    return tok, ast
            return tok0, None

        return parse

    gspec = defaultdict(list)
    for rule in rules:
        lhs, _, rhs = rule.partition(":=")
        gspec[lhs.strip()].append(rhs.strip().split())
    g = {k: one_rule(k, v) for k, v in gspec.items()}
    return g["<top>"]


my_expr_lexer = make_lexer(
    [
        ("<skip>", r"\s*"),
        ("<self>", r"[-+*()]"),
        ("number", r"[0-9]+"),
    ]
)


my_expr_parser = make_parser(
    [
        "<top> := <add>",
        "<add> := <mul> + <add>",
        "<add> := <mul> - <add>",
        "<add> := <mul>",
        "<mul> := <term> * <mul>",
        "<mul> := <term>",
        "<term> := number",
        "<term> := ( <add> )",
    ]
)


def expr_eval(ast):
    print("eval", ast)
    if ast[0] == "<add>":
        if ast[2] == "+":
            return expr_eval(ast[1]) + expr_eval(ast[3])
        elif ast[2] == "-":
            return expr_eval(ast[1]) - expr_eval(ast[3])
    if ast[0] == "<mul>":
        return expr_eval(ast[1]) * expr_eval(ast[3])
    if ast[0] == "<term>":
        return int(ast[1])


def expr_invert(ast):
    print("invert", ast)
    if ast[0] == "<add>" or ast[0] == "<mul>":
        return f"{expr_invert(ast[1])} {expr_invert(ast[3])} {ast[2]}"
    if ast[0] == "<term>":
        return ast[1]


def example(s):
    tok, ast = my_expr_parser(list(my_expr_lexer(s)))
    print(expr_eval(ast))
    print(expr_invert(ast))


args = list(sys.argv[1:])
if len(args) == 0:
    args = ["(2 + 3) * (4 + 5)"]
for s in args:
    example(s)