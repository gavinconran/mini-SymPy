"""Contains the Class Expression and associated sub-classes."""

from numbers import Number
import numpy as np

class Expression:
    """Expression class represengts an algebriac expression."""

    def __init__(self, operands):
        """Expression class constructor method."""
        self.operands = operands

    def __add__(self, other):
        """Add Expression self to Expression other or number other."""
        raise NotImplemented

    def __radd__(self, other):
        """Add Expression other to Number self."""
        raise NotImplemented

    def __sub__(self, other):
        """Subtract Expression or Number other from Expression self."""
        raise NotImplemented

    def __rsub__(self, other):
        """Subtract Expression other from Number self."""
        raise NotImplemented

    def __mul__(self, other):
        """Multiply Expression self from Expression other or Number other."""
        raise NotImplemented

    def __rmul__(self, other):
        """Multiply Number self with Expression other."""
        raise NotImplemented

    def __div__(self, other):
        """Divide Expression self by Expression other or Number other."""
        raise NotImplemented

    def __rtruediv__(self, other):
        """Divide Number self with Expression other."""
        raise NotImplemented

    def __pow__(self, other):
        """Raise Expression self to the power Expression or Number other."""
        raise NotImplemented


class Operator(Expression):
    """Operator class."""

    def __repr__(self):
        """Return the canonical representation of an operator."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        """Return a string representation of the Operator."""
        raise NotImplemented


class Add(Expression):
    """Add class"""

    precedence = 2
    symbol = '+'


class Sub(Expression):
    """Subtract class"""

    precedence = 2
    symbol = '-'    


class Mul(Expression):
    """Multiply class"""

    precedence = 1
    symbol = '*'


class Div(Expression):
    """Divide class"""

    precedence = 1
    symbol = '/'


class Pow(Expression):
    """Power class"""

    precedence = 3
    symbol = '+'


class Terminal(Expression):
    """Terminal Class"""

    def __init__(self, operands):
        """Operator class constructor method."""
        return super().__init__(operands)

    def __repr__(self):
        """Return the canonical representation of the Terminal."""
        return repr(self.value)

    def __str__(self):
        """Return a string representation of the Terminal."""
        return str(self.value)


class Number(Expression):
    """Number class"""

    def __init__(self, value):
        """Number class constructor method."""
        if isinstance(value, Number):
            self.value = value
        return super().__init__(())


class Symbol(Expression):
    """Symbol class"""

    def __init__(self, value):
        """Symbol class constructor method."""
        if isinstance(value, str):
            self.value = value
        return super().__init__(())






