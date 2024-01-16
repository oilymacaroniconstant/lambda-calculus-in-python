#!/usr/bin/env python3
import string

# tristan was hier


class LambdaTerm:
    """Abstract Base Class for lambda terms."""
    @staticmethod
    def fromnumber(number):
        if number == 0:
            return nul
        else:
            # string maken --> fromstring()
            return None

    def successor(number):
        return None

    @staticmethod
    def fromstring(string):
        """Construct a lambda term from a string."""

        # input: 'x', '(M N)', '(lx.M)'
        # output: Variable('x'), Application(M, N), Abstraction(x, M) using recursion?

        new_string_list = string.split(' ')

        for i in range(len(new_string_list)):
            if new_string_list[i][0] == 'l':
                variable = Variable(new_string_list[i][1])
                body = LambdaTerm.fromstring(new_string_list[i][3:])
                new_string_list[i] = Abstraction(variable, body)
            else:
                new_string_list[i] = Variable(new_string_list[i])

        for i in range(len(new_string_list)-1):
            new_string_list[0] = Application(
                new_string_list[0], new_string_list[1+i])

        output = new_string_list[0]
        return output

    def reduce(self):
        """Beta-reduce."""
        # loop/recursie met substitutie functie erop toegepast
        lijst = [self.substitute()]
        while True:
            lijst.append(lijst[-1].substitute())
            if str(lijst[-2]) == str(lijst[-1]):
                break
        return lijst[-1]

    def __eq__(self, other):
        """alpha-equivalence"""
        self = str(self.reduce())
        other = str(other.reduce())

        letters_self = ''
        letters_other = ''

        database = string.ascii_letters
        used_letters_self = []
        used_letters_other = []

        if len(self) != len(other):
            return False

        for i in range(len(self)):
            if self[i] not in used_letters_self:
                if self[i] in database:
                    letters_self += self[i]
                    used_letters_self.append(self[i])

        for i in range(len(other)):
            if other[i] not in used_letters_other:
                if other[i] in database:
                    letters_other += other[i]
                    used_letters_other.append(other[i])

        for i in range(len(used_letters_self)):
            self = self.replace(letters_self[i], database[i])
            other = other.replace(letters_other[i], database[i])

        if self == other:
            return True
        else:
            return False


class Variable(LambdaTerm):
    """Represents a variable."""

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return self.symbol

    def __str__(self):
        return self.symbol

    def substitute(self):
        return self


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form (λx.M)."""

    def __init__(self, variable, body):
        self.variable = variable
        self.body = body

    def __repr__(self):
        return f'λ{self.variable.symbol}.{self.body.symbol}'

    def __str__(self):
        return f'λ{self.variable.symbol}:.{self.body.symbol}'

    def __call__(self, argument): raise NotImplementedError

    def substitute(self, argument):
        if self.variable.symbol == self.body.symbol:
            return argument
        else:
            return self.body


class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    def __init__(self, function, argument):
        self.function = function
        self.argument = argument

    def __repr__(self):
        return f'({str(self.function)} {str(self.argument)})'

    def __str__(self):
        return f'({str(self.function)} {str(self.argument)})'

    def substitute(self):
        # Check type compatibility first
        if isinstance(self.function, Abstraction):
            return self.function.substitute(self.argument)
        else:
            return Application(self.function.substitute(), self.argument)


# Own programming language
# Natural numbers
nul = Abstraction(Variable('s'), Abstraction(
    Variable('z'), Variable('z')))


x = Variable('x')
y = Variable('y')
abstractie = Abstraction(x, x)
applicatie = Application(abstractie, y)

print(LambdaTerm.fromstring('lx.y q ly.y z')
      == LambdaTerm.fromstring('x lx.x q'))
