"""Contains the Class Expression and associated sub-classes."""

import numbers


class Expression:
    """Expression class represengts an algebriac expression."""

    def __init__(self, operands):
        """Expression class constructor method."""
        self.o = operands

    def __add__(self):
        """Add operand 1 to operand 2."""
        return self.__repr__()

    def __sub__(self):
        """Subtract operand 2 from operand 1."""
        return self.__repr__()

    def __mul__(self):
        """Multiply operand 1 by operand 2."""
        return self.__repr__()

    def __div__(self):
        """Divide operand 1 by operand 2."""
        return self.__repr__()

    def __pow__(self):
        """Divide operand 1 by operand 2."""
        return self.__repr__()


class Operator(Expression):
    """Operator class."""

    def __repr__(self):
        """Return the canonical representation of an operator."""
        return type(self).__name__ + repr(self.o)

    def __str__(self):
        """Return a string representation of the Operator."""
        return f'{self.o[0]} {self.symbol} {self.o[1]}'


class Add(Operator):
    """Add class."""

    precedence = 2
    symbol = '+'

    def __init__(self, x, y):
        super().__init__((x, y))
        super().__add__()


class Sub(Operator):
    """Subtraction class."""

    precedence = 2
    symbol = '-'

    def __init__(self, x, y):
        super().__init__((x, y))
        super().__sub__()


class Mul(Operator):
    """Multiply class."""

    symbol = '*'

    def __init__(self, x, y):
        super().__init__((x, y))
        super().__mul__()


class Div(Operator):
    """Divide class."""

    symbol = '/'

    def __init__(self, x, y):
        super().__init__((x, y))
        super().__div__()


class Pow(Operator):
    """power class."""

    symbol = '^'

    def __init__(self, x, y):
        super().__init__((x, y))
        super().__pow__()


class Terminal(Expression):
    """Terminal Class."""

    def __init__(self, value):
        """Operator class constructor method."""
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
        """Initialise a number."""
        if isinstance(value, numbers.Number):
            super().__init__(value)
        else:
            raise ValueError


class Symbol(Terminal):
    """Symbol class."""

    def __init__(self, op):
        """Initialise a symbol."""
        if isinstance(op, str):
            super().__init__(op)
        else:
            raise ValueError
