from graphviz import Digraph


class Expression:
    def to_graph(self, graph: Digraph | None = None) -> tuple[str, Digraph]:
        raise NotImplementedError()

    def evaluate(self):
        raise NotImplementedError()


class BinaryExpression(Expression):
    operator: str = ""

    def __init__(self, left: Expression, right: Expression) -> None:
        self.left = left
        self.right = right

    def to_graph(self, graph: Digraph | None = None) -> tuple[str, Digraph]:
        if graph is None:
            graph = Digraph()

        left_id, _ = self.left.to_graph(graph)
        right_id, _ = self.right.to_graph(graph)

        self_id = f"{id(self)}"
        graph.node(self_id, self.operator)
        graph.edge(self_id, left_id)
        graph.edge(self_id, right_id)

        return self_id, graph


class Add(BinaryExpression):
    operator = "+"

    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()


class Sub(BinaryExpression):
    operator = "-"

    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()


class Mult(BinaryExpression):
    operator = "*"

    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()


class Div(BinaryExpression):
    operator = "/"

    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()


class Atom(Expression):
    def __init__(self, lex: str) -> None:
        self.lex = lex

    def to_graph(self, graph: Digraph | None = None) -> tuple[str, Digraph]:
        if graph is None:
            graph = Digraph()

        graph.node(str(id(self)), self.lex)

        return str(id(self)), graph


class Number(Atom):
    def evaluate(self):
        return int(self.lex) if self.lex.isdigit() else float(self.lex)
