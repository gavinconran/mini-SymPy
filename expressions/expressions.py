"""Contains the Class Expression and associated sub-classes."""

import numbers


class Expression:
    """Expression class."""

    def __init__(self, operands):
        """Initialise an expresiion."""
        self.o = operands

    def __add__(self, other):
        """Return the Expr for the sum of this Expr and another."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        if isinstance(self, numbers.Number):
            self = Number(self)
        return Add(self, other)

    def __sub__(self, other):
        """Return the Expr for the sub of this Expr and another."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        if isinstance(self, numbers.Number):
            self = Number(self)
        return Sub(self, other)

    def __mul__(self, other):
        """Return the Expr for the mul of this Expr and another."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        if isinstance(self, numbers.Number):
            self = Number(self)
        return Mul(self, other)

    def __div__(self, other):
        """Return the Expr for the div of this Expr and another."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        if isinstance(self, numbers.Number):
            self = Number(self)
        return Div(self, other)

    def __pow__(self, other):
        """Return the Expr for the pow of this Expr and another."""
        if isinstance(other, numbers.Number):
            other = Number(other)
        if isinstance(self, numbers.Number):
            self = Number(self)
        return Pow(self, other)


class Operator(Expression):
    """Operator class."""

    def __repr__(self):
        """Return the canonical representation of an operator."""
        return type(self).__name__ + repr(self.o)

    def __str__(self):
        """Return a string representation of the Operator."""
        left_str = " ".join(map(str, self.o[:len(self.o) - 2]))
        return f'{left_str} {self.symbol} {self.o[-1]}'


def make_operands_tuple(left, symbol, right):
    """Help function."""
    if isinstance(left, Terminal):
        operands_list = [left.value, symbol, right.value]
    else:
        operands_list = [item for item in left.o]
        operands_list.append(symbol)
        operands_list.append(right.value)
    return tuple(operands_list)


class Add(Operator):
    """Addition class."""

    precedence = 2
    symbol = '+'

    def __init__(self, left, right):
        """Construct an Add object."""
        self.o = make_operands_tuple(left, self.symbol, right)
        Expression(self.o)


class Sub(Operator):
    """Subtract class."""

    precedence = 2
    symbol = '-'

    def __init__(self, left, right):
        """Construct a Sub object."""
        self.o = make_operands_tuple(left, self.symbol, right)
        Expression(self.o)


class Mul(Operator):
    """Multiply class."""

    precedence = 1
    symbol = '*'

    def __init__(self, left, right):
        """Construct a Mul object."""
        self.o = make_operands_tuple(left, self.symbol, right)
        Expression(self.o)


class Div(Operator):
    """Divide class."""

    precedence = 1
    symbol = '/'

    def __init__(self, left, right):
        """Construct n Div object."""
        self.o = make_operands_tuple(left, self.symbol, right)
        Expression(self.o)


class Pow(Operator):
    """Power class."""

    precedence = 3
    symbol = '^'

    def __init__(self, left, right):
        """Construct an Pow object."""
        self.o = make_operands_tuple(left, self.symbol, right)
        Expression(self.o)


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
