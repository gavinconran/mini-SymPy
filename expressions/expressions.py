"""Contains the Class Expression and associated sub-classes."""

import numbers
from functools import wraps, singledispatch


def make_other_expr(meth):
    """Cast the second argument of a method of Number when neded."""
    @wraps(meth)
    def fn(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        if isinstance(self, numbers.Number):
            self = Number(self)
        return meth(self, other)
    return fn


class Expression:
    """Expression class."""

    def __init__(self, operands):
        """Initialise an Expression."""
        self.operands = operands
        self.parentheses = False

    @make_other_expr
    def __add__(self, other):
        """Return the Expr for the sum of this Expr and another."""
        return Add(self, other)

    @make_other_expr
    def __radd__(self, other):
        """Add Expression other to number self."""
        return Add(other, self)

    @make_other_expr
    def __sub__(self, other):
        """Return the Expr for the sub of this Expr and another."""
        return Sub(self, other)

    @make_other_expr
    def __rsub__(self, other):
        """Subtract Expression other from number self."""
        return Sub(other, self)

    @make_other_expr
    def __mul__(self, other):
        """Return the Expr for the mul of this Expr and another."""
        return Mul(self, other)

    @make_other_expr
    def __rmul__(self, other):
        """Multiply Expression by number self."""
        return Mul(other, self)

    @make_other_expr
    def __truediv__(self, other):
        """Return the Expr for the div of this Expr and another."""
        return Div(self, other)

    @make_other_expr
    def __rtruediv__(self, other):
        """Divide Expression other by number self."""
        return Div(other, self)

    @make_other_expr
    def __pow__(self, other):
        """Return the Expr for the pow of this Expr and another."""
        return Pow(self, other)

    @make_other_expr
    def __rpow__(self, other):
        """Return the Expr for the pow of this Expr and another."""
        return Pow(other, self)


class Operator(Expression):
    """Operator class."""

    def __repr__(self):
        """Return the canonical representation of an operator."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        """Return a string representation of the Operator."""
        if self.parentheses:
            return (f'({self.operands[0]} {self.symbol} {self.operands[1]})')
        else:
            return (f'{self.operands[0]} {self.symbol} {self.operands[1]}')


def check_for_precedence(operand, operator):
    """Check for precedence."""
    return not isinstance(operand, Terminal) \
        and operand.precedence < operator.precedence


class Add(Operator):
    """Addition class."""

    precedence = 1
    symbol = '+'

    def __init__(self, left, right):
        """Construct an Add object."""
        self.parentheses = False
        self.operands = (left, right)


class Sub(Operator):
    """Subtract class."""

    precedence = 1
    symbol = '-'

    def __init__(self, left, right):
        """Construct a Sub object."""
        self.parentheses = False
        self.operands = (left, right)


class Mul(Operator):
    """Multiply class."""

    precedence = 2
    symbol = '*'

    def __init__(self, left, right):
        """Construct a Mul object."""
        self.parentheses = False
        if check_for_precedence(left, self):
            left.parentheses = True
        if check_for_precedence(right, self):
            right.parentheses = True
        self.operands = (left, right)


class Div(Operator):
    """Divide class."""

    precedence = 2
    symbol = '/'

    def __init__(self, left, right):
        """Construct an Div object."""
        self.parentheses = False
        if check_for_precedence(left, self):
            left.parentheses = True
        if check_for_precedence(right, self):
            right.parentheses = True
        self.operands = (left, right)


class Pow(Operator):
    """Power class."""

    precedence = 3
    symbol = '^'

    def __init__(self, left, right):
        """Construct an Pow object."""
        self.parentheses = False
        if check_for_precedence(left, self):
            left.parentheses = True
        if check_for_precedence(right, self):
            right.parentheses = True
        self.operands = (left, right)


class Terminal(Expression):
    """Terminal class."""

    def __init__(self, value):
        super().__init__(())
        self.value = value

    def __repr__(self):
        """Return the canonical representation of the Terminal."""
        return repr(self.value)

    def __str__(self):
        """Return a string representation of the Terminal."""
        return str(self.value)


class Number(Terminal):
    """Number class."""

    def __init__(self, value):
        if isinstance(value, numbers.Number):
            super().__init__(value)
        else:
            raise ValueError


class Symbol(Terminal):
    """Symbol class."""

    def __init__(self, value):
        if isinstance(value, str):
            super().__init__(value)
        else:
            raise ValueError


def postvisitor(expr, fn, **kwargs):
    """Visit an Expression in postorder applying a function to every node.

    Parameters
    ----------
    expr: Expression
        The expression to be visited.
    fn: `function(node, *o, **kwargs)`
        A function to be applied at each node. The function should take
        the node to be visited as its first argument, and the results of
        visiting its operands as any further positional arguments. Any
        additional information that the visitor requires can be passed in
        as keyword arguments.
    **kwargs:
        Any additional keyword arguments to be passed to fn.
    """
    stack = []
    visited = {}
    stack.append(expr)
    while stack:
        e = stack.pop()
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)

        if unvisited_children:
            stack.append(e)  # Not ready to visit this node yet.
            # Need to visit children before e.
            for child in unvisited_children:
                stack.append(child)
        else:
            # Any children of e have been visited, so we can visit it.
            visited[e] = fn(e, *(visited[o] for o in e.operands),
                            **kwargs)

    # When the stack is empty, we have visited every subexpression,
    # including expr itself.
    return visited[expr]


@singledispatch
def differentiate(expr, *o, **kwargs):
    """Differentiate an expression node.

    Parameters
    ----------
    expr: Expression
        The expression node to be evaluated.
    *o: Number
        The results of differentiating the operands of expr.
    **kwargs:
        Any keyword arguments required to differentiating specific types of
        expression.
    wrt_var: character
        The variable with respect to differentiation, for
        example:        'x'
    """
    raise NotImplementedError(
        f"Cannot evaluate a {type(expr).__name__}")


@differentiate.register(Number)
def _(expr, *o, **kwargs):
    return 0.0


@differentiate.register(Symbol)
def _(expr, *o, **kwargs):
    if kwargs['var'] == expr.value:
        return 1.0
    else:
        return 0.0


@differentiate.register(Add)
def _(expr, *o, **kwargs):
    return o[0] + o[1]


@differentiate.register(Sub)
def _(expr, *o, **kwargs):
    return o[0] - o[1]


@differentiate.register(Mul)
def _(expr, *o, **kwargs):
    # product rule
    return o[0] * expr.operands[1] + o[1] * expr.operands[0]


@differentiate.register(Div)
def _(expr, *o, **kwargs):
    # quodient rule
    return (o[0] * expr.operands[1] - expr.operands[0] * o[1]) \
            / expr.operands[1] ** 2


@differentiate.register(Pow)
def _(expr, *o, **kwargs):
    # chain rule for powers
    res = expr.operands[1] * expr.operands[0] ** (expr.operands[1] - 1) * 1.0
    return res
