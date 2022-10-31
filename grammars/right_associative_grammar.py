import grammars.astnodes as ast

from pyjapt import Grammar

g = Grammar()

expr = g.add_non_terminal("expr", True)
term, fact = g.add_non_terminals("term fact")

g.add_terminals("+ - / * ( )")
g.add_terminal("int", regex=r"\d+(\.\d+)?")


@g.terminal("whitespace", r" +")
def whitespace(_lexer):
    _lexer.column += len(_lexer.token.lex)
    _lexer.position += len(_lexer.token.lex)


expr %= "term + expr", lambda s: ast.Add(s[1], s[3])
expr %= "term - expr", lambda s: ast.Sub(s[1], s[3])
expr %= "term", lambda s: s[1]

term %= "fact * term", lambda s: ast.Mult(s[1], s[3])
term %= "fact / term", lambda s: ast.Div(s[1], s[3])
term %= "fact", lambda s: s[1]

fact %= "( expr )", lambda s: s[2]
fact %= "int", lambda s: ast.Number(s[1])

lexer = g.get_lexer()
parser = g.get_parser("slr")
