#!/usr/bin/env python3

# tristan was hier

class LambdaTerm:
    """Abstract Base Class for lambda terms."""

    def fromstring(self):
        """Construct a lambda term from a string."""
        raise NotImplementedError

    def substitute(self, rules):
        """Substitute values for keys where they occur."""
        raise NotImplementedError

    def reduce(self):
        """Beta-reduce."""
        # loop/recursie met substitutie functie erop toegepast


class Variable(LambdaTerm):
    """Represents a variable."""

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self): raise NotImplementedError

    def __str__(self):
        return self.symbol

    def substitute(self, rules):
        return self


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    def __init__(self, variable, body):
        self.variable = variable
        self.body = body

    def __repr__(self): raise NotImplementedError

    def __str__(self):
        return f'λ{self.variable}.{self.body}'

    def __call__(self, argument): raise NotImplementedError

    def substitute(self, rules): raise NotImplementedError


class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    def __init__(self, function, argument): raise NotImplementedError

    def __repr__(self): raise NotImplementedError

    def __str__(self): raise NotImplementedError

    def substitute(self, rules): raise NotImplementedError

    def reduce(self): raise NotImplementedError


x = Variable('x')
y = Variable('y')
x.fromstring()
abstractie = Abstraction(x, y)

print(x)
