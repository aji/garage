from collections import namedtuple as NT
from collections import defaultdict


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
            print("parse", lhs, " ".join(v for tt, v in tok0))
            for rhs in rhses:
                tok, ast = one_rhs(tok0, rhs)
                if ast is not None:
                    return tok, ast
            return tok0, None

        return parse

    gspec = defaultdict(list)
    for rule in rules:
        lhs, _, rhs = rule.partition(":=")
        gspec[lhs.strip()].append(rhs.strip().split())
    g = {k: one_rule(k, v) for k, v in gspec.items()}
    return g["<top>"]


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


def example():
    tok0 = [
        ("(", "("),
        ("number", "2"),
        ("+", "+"),
        ("number", "3"),
        (")", ")"),
        ("*", "*"),
        ("(", "("),
        ("number", "4"),
        ("+", "+"),
        ("number", "5"),
        (")", ")"),
    ]
    tok, ast = my_expr_parser(tok0)
    print(expr_eval(ast))
    print(expr_invert(ast))


example()