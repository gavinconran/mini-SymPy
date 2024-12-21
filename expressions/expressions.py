"""Contains the Class Expression and associated sub-classes."""

import numbers


class Expression:
    """Expression class represengts an algebriac expression."""

    def __init__(self, x, y):
        """Expression class constructor method."""
        self.x = x
        self.y = y

    def __add__(self):
        """Add Expression self to Expression other or number other."""
        return self.x + self.y

    def __radd__(self, *o):
        """Add Expression other to Number self."""
        return self.x + self.y   


class Operator(Expression):
    """Operator class."""

    def __repr__(self):
        """Return the canonical representation of an operator."""
        return repr(self.x) + " " + type(self).symbol + " " + repr(self.y)


    def __str__(self):
        """Return a string representation of the Operator."""
        if self.symbol == "+":
            return f'{self.x} {self.symbol} {self.y}'
        else:
            return self.symbol   


class Add(Operator):
    """Add class."""

    precedence = 2
    symbol = '+'

    def __init__(self, x, y):
        """Constructor."""
        super().__init__(x, y)
        super().__add__()


class Terminal(Expression):
    """Terminal Class."""

    def __init__(self, value):
        """Operator class constructor method."""
        super().__init__(0, 0)
        self.value = value

    def __repr__(self):
        """Return the canonical representation of the Terminal."""
        return repr(self.value)

    def __str__(self):
        """Return a string representation of the Terminal."""
        return str(self.value)


class Number(Terminal):
    """Number class"""

    def __init__(self, value):
        """Constructor"""
        if isinstance(value, numbers.Number):
            super().__init__(value)
        else:
            raise ValueError


class Symbol(Terminal):
    """Symbol class"""

    def __init__(self, op):
        """Constructor"""
        if isinstance(op, str):
            super().__init__(op)
        else:
            raise ValueError
