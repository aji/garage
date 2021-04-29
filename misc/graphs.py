from collections import namedtuple as NT
from collections import defaultdict


def make_parser(rules):
    def one_rule(lhs, rhses):
        def one_rhs(tok0, rhs):
            tok = tok0
            ast = [lhs]
            for i, term in enumerate(rhs):
                if len(tok) == 0:
                    return tok0, None
                if term in g.keys():
                    tok, v = g[term](tok)
                    if v is None:
                        return tok0, None
                else:
                    tt, v = tok[0]
                    tok = tok[1:]
                    if tt != term:
                        return tok0, None
                ast.append(v)
            return tok, ast

        def parse(tok0):
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


my_expr_rules = [
    "<top> := <add>",
    "<add> := <mul> + <add>",
    "<add> := <mul> - <add>",
    "<add> := <mul>",
    "<mul> := <term> * <mul>",
    "<mul> := <term>",
    "<term> := number",
    "<term> := ( <add> )",
]

print(
    make_parser(my_expr_rules)(
        [
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
    )
)
