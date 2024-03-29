import string
import time


class LambdaTerm:
    """Abstract Base Class for lambda terms."""

##########################################################################################################################################
####### BASIC FUNCTIONS #######
##########################################################################################################################################

    @staticmethod
    def fromString(string):
        """Construct a lambda term from a string."""

        def fromStringtoRepr(string2):
            for i, j in enumerate(string2):
                if j == 'λ':
                    return f"Abstraction(Variable('{string2[i+1]}'), {fromStringtoRepr(string2[i+3:])})"
                elif j == '(':
                    tracker = 0
                    for k, l in enumerate(string2[i+1:]):
                        if l == '(':
                            tracker += 1
                        elif l == ')':
                            tracker -= 1
                        elif l == ' ':
                            if tracker == 0:
                                return f"Application({fromStringtoRepr(string2[i+1:k+1])}, {fromStringtoRepr(string2[k+2:-1])})"

                else:
                    return f"Variable('{j}')"

        return eval(fromStringtoRepr(string))

    @staticmethod
    def alphaConversion(**kwargs):
        """Change the symbols in your lambda term with new ones.\n
        \n
        The first argument has to be a lambda term and the following arguments should be the symbols you want to replace and the symbols replacing that symbol in alternating fashion.\n
        \n
        Example: LambdaTerm.alphaConversion(LambdaTerm=F, symbol='a', replacesymbol='e', symbol2='b', replacesymbol2='f')"""

        keys = list(kwargs)
        values = list(kwargs.values())

        for i in range(1, len(keys), 2):
            LambdaTerm_repr = repr(values[0])
            # We want to replace the letters in quotation marks: 'a', 'x' etc.
            LambdaTerm_repr = LambdaTerm_repr.replace(
                f"'{values[i]}'", f"'{values[i+1]}'")
            values[0] = eval(LambdaTerm_repr)

        return eval(LambdaTerm_repr)

    def reduce(self):
        """Beta-reduce."""

        # loop/recursion while applying the substitute function. If the previous substitute gives the same one as the current, then return (i.e. if it is nonreducible).

        lijst = [self.substitute()]
        while True:
            lijst.append(lijst[-1].substitute())
            if repr(lijst[-2]) == repr(lijst[-1]):
                break
        return lijst[-1]

    def __eq__(self, other):
        self = str(self.reduce())
        other = str(other.reduce())
        if len(self) != len(other):
            return False
        lijst = []
        for i in range(len(self)):
            lijst.append([self[i], other[i]])
            if i > 0:
                for j in range(i-1):
                    if lijst[j][0] == self[i] and lijst[j][1] != other[i]:
                        return False
                    elif lijst[j][0] != self[i] and lijst[j][1] == other[i]:
                        return False
        return True


##########################################################################################################################################
####### ARITHEMTIC #######
##########################################################################################################################################

    @staticmethod
    def successor(number):
        '''Adds one to the given number and returns its lambda term'''

        if isinstance(number, Abstraction):
            return Abstraction(Variable('w'), Abstraction(Variable('y'), Abstraction(Variable('x'), Application(Variable('y'), Application(Application(Variable('w'), Variable('y')), Variable('x'))))))(number).reduce()
        else:
            return Abstraction(Variable('w'), Abstraction(Variable('y'), Abstraction(Variable('x'), Application(Variable('y'), Application(Application(Variable('w'), Variable('y')), Variable('x'))))))(LambdaTerm.fromNumber(number)).reduce()

    @staticmethod
    def fromNumber(number):
        '''Converts a number to its lambda term representation'''

        if number == 0:
            return zero
        else:
            output = LambdaTerm.successor(zero).reduce()
            for i in range(number-1):
                output = LambdaTerm.successor(output).reduce()
            return output

    @staticmethod
    def toNumber(LambdaTerm):
        '''Converts a lambda term to its base 10 number representation'''
        # NOTE: It doesn't check if LambdaTerm is a valid number defined above.

        if LambdaTerm == zero:
            return 0
        else:
            count = repr(LambdaTerm).count('Variable')
            return count-3

    def __add__(self, other):
        '''Adds two numbers represented as lambda terms'''
        # NOTE: It doesn't check if self and other are valid numerical lambda terms as defined above.

        # Apply the successor function 'self' times. We chose this method instead of the naive method, due to lower computation time.

        self_number = LambdaTerm.toNumber(self)
        other_number = LambdaTerm.toNumber(other)

        if self_number < other_number:
            for i in range(self_number):
                other = LambdaTerm.successor(other)
            return other
        else:
            for i in range(other_number):
                self = LambdaTerm.successor(self)
            return self

    def __mul__(self, other):
        '''Multiplication of two (lambda) numbers x and y'''

        return (Abstraction(Variable('x'), Abstraction(Variable('w'), Abstraction(Variable('y'), Application(Variable('x'), Application(Variable('w'), Variable('y'))))))(self).reduce())(other).reduce()


class Variable(LambdaTerm):
    """Represents a variable."""

    def __init__(self, symbol):
        self.symbol = symbol

    def __repr__(self):
        return f"Variable('{self.symbol}')"

    def __str__(self):
        return self.symbol

    def substitute(self):
        return self


class Abstraction(LambdaTerm):
    """Represents a lambda term of the form λx.M."""

    def __init__(self, variable, body):
        self.variable = variable
        self.body = body

    def __repr__(self):
        return f'Abstraction({repr(self.variable)}, {repr(self.body)})'

    def __str__(self):
        return f'λ{str(self.variable)}.{str(self.body)}'

    def __call__(self, argument):
        return Application(self, argument).reduce()

    def substitute(self, argument='0'):
        # λx.M: Checks if an argument was given. If an argument was given, then replace the body of the abstraction by the argument and return only that body. Else return itself with its argument reduced (if possible).

        if str(argument) != '0':
            self_repr = repr(self.body).replace(
                repr(self.variable), repr(argument))
            return eval(self_repr)
        else:
            return Abstraction(self.variable, self.body.substitute())


class Application(LambdaTerm):
    """Represents a lambda term of the form (M N)."""

    def __init__(self, function, argument):
        self.function = function
        self.argument = argument

    def __repr__(self):
        return f'Application({repr(self.function)}, {repr(self.argument)})'

    def __str__(self):
        return f'({str(self.function)} {str(self.argument)})'

    def substitute(self):
        # (M N): Check type compatibility first: argument is only substitutable if M is an abstraction. If M is an abstraction, substitute the argument. Else return itself with its arguments reduced (if possible).

        if isinstance(self.function, Abstraction):
            return self.function.substitute(self.argument)
        else:
            return Application(self.function.substitute(), self.argument.substitute())


######################################################################################################
####### BASIC DEFINITIONS #######
######################################################################################################

# 0
zero = LambdaTerm.fromString('λs.λf.f')

# The identity function
I = LambdaTerm.fromString('λx.x')

# The successor function. Will need it later.
successor = LambdaTerm.fromString('λw.λy.λx.(y ((w y) x))')


######################################################################################################
####### CONDITIONALS #######
######################################################################################################

# True
T = LambdaTerm.fromString('λc.λd.c')

# False
F = LambdaTerm.fromString('λa.λb.b')

# λx.(λy.((x y) F))
And = LambdaTerm.fromString(f'λr.λs.((r s) λp.λq.q)')

# λx.(λy.((x T) y))
Or = LambdaTerm.fromString(f'λt.λu.((t λv.λw.v) u)')

# λx.((x F) T)
negation = LambdaTerm.fromString(f'λx.((x λe.λf.f) λg.λh.g)')


# 0: True, other numbers are false.
# λi.(((i F) negation) F)
conditional_test = LambdaTerm.fromString(
    f'λi.(((i λj.λk.k) {negation}) λl.λm.m)')


# NOTE: Not usable (yet)
# phi generates from the pair p = (n,n-1) the pair (n+1,n-1)
phi = LambdaTerm.fromString(
    f'λp.λz.((z ({successor} (p {T}))) (p {T}))')

# NOTE: Not usable (yet)
# the predecessor of a number n. Applies the phi n times to (λz.((z 0) 0)) and then selects the second member of the pair
P = LambdaTerm.fromString(
    f'(λn.((n {phi}) λe.((e {zero}) {zero})) {F})')


######################################################################################################
####### RECURSION #######
######################################################################################################

# This is untyped lambda calculus, so recursion will not terminate.
recursion = LambdaTerm.fromString('λn.(λo.(n (o o)) λo.(n (o o)))')

# NOTE: Not usable (yet)
recursive_sum = LambdaTerm.fromString(
    f'λr.λn.((({conditional_test} n) {zero}) ((n {successor}) (r ({P} n))))')
