"""Contains the Class Expression and associated sub-classes."""

import numbers
from functools import wraps


def make_other_expr(meth):
    """Cast the second argument of a method of Number when neded."""
    @wraps(meth)
    def fn(self, other):
        if isinstance(other, numbers.Number):
            other = Number(other)
        return meth(self, other)
    return fn


class Expression:
    """Expression class."""

    def __init__(self, operands):
        """Initialise an Expression."""
        self.o = operands

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
        operands = tuple([self.o[i] for i in range(len(self.o)) if i % 2 == 0])
        return type(self).__name__ + repr(operands)

    def __str__(self):
        """Return a string representation of the Operator."""
        #### HERE IS THE BUG ###
        expr_str = " ".join(map(str, self.o))
        return f'{expr_str}'


def make_operands_tuple(left, operator, right):
    """Auxillory function."""
    if isinstance(left, Terminal): # left is Terminal
        if isinstance(right, Terminal): # left is Terminal, right is Terminal
            operands_list = [left.value, operator.symbol, right.value]
        else: # left is Terminal, right is an Operator
            operands_list = [left.value, operator.symbol]
            for item in right.o:
                operands_list.append(item)
            if (operator.precedence < right.precedence):
                print('Add brackets to right Operator')
                operands_list.insert(0, '(')
                operands_list.append(')')
                print(f'right Operator: {tuple(operands_list)}')    
            right.o = tuple(operands_list)
    else: # left is Operator
        # As left is an Operator, check for higher precedence
        #### HERE IS THE BUG ###
        if (left.precedence < operator.precedence):
            print('Add brackets to left Operator')
            left_list = ['(']
            for item in left.o:
                left_list.append(item)
            left_list.append(')')
            print(f'left Operator: {tuple(left_list)}')
            left.o = tuple(left_list)

        if isinstance(right, Terminal): # left is Opeator, right is Terminal
            operands_list = [item for item in left.o]
            operands_list.append(operator.symbol)
            operands_list.append(right.value)
        else: # left is a Operator, right is a Operator
            operands_list = [item for item in left.o]
            operands_list.append(operator.symbol)
            for item in right.o:
                operands_list.append(item)
    return tuple(operands_list)


class Add(Operator):
    """Addition class."""

    precedence = 1
    symbol = '+'

    def __init__(self, left, right):
        """Construct an Add object."""
        self.o = make_operands_tuple(left, self, right)


class Sub(Operator):
    """Subtract class."""

    precedence = 1
    symbol = '-'

    def __init__(self, left, right):
        """Construct a Sub object."""
        self.o = make_operands_tuple(left, self, right)


class Mul(Operator):
    """Multiply class."""

    precedence = 2
    symbol = '*'

    def __init__(self, left, right):
        """Construct a Mul object."""
        self.o = make_operands_tuple(left, self, right)


class Div(Operator):
    """Divide class."""

    precedence = 2
    symbol = '/'

    def __init__(self, left, right):
        """Construct an Div object."""
        self.o = make_operands_tuple(left, self, right)


class Pow(Operator):
    """Power class."""

    precedence = 3
    symbol = '^'

    def __init__(self, left, right):
        """Construct an Pow object."""
        self.o = make_operands_tuple(left, self, right)


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
