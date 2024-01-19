#!/usr/bin/env python3
from sympy import sympify, symbols
import string


class LambdaTerm:
    """Abstract Base Class for lambda terms."""

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
        # NOTE: We don't check if LambdaTerm is a valid number defined above.

        if LambdaTerm == zero:
            return 0
        else:
            count = 0
            for i in str(LambdaTerm):
                # Our choice of the variable name 'y' is arbitrary. This is due to how we defined the successor function.
                if i == 'y':
                    count += 1
            return count-1

    def __add__(self, other):
        '''Converts a lambda term to its base 10 number representation'''
        # NOTE: We don't check if self and other are valid numerical lambda terms as defined above.

        # Apply the successor function 'self' times. Chose this method due to lower computation time.
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
        # multiplication of two numbers x and y

        return (Abstraction(Variable('x'), Abstraction(Variable('w'), Abstraction(Variable('y'), Application(Variable('x'), Application(Variable('w'), Variable('y'))))))(self).reduce())(other).reduce()


##########################################################################################################################################
####### BASIC FUNCTIONS #######
##########################################################################################################################################

####################################################################################################################################################################################################################################################################################

    @staticmethod
    def fromString(string):
        """Construct a lambda term from a string."""

        # input: 'x', '(M N)', '(lx.M)'
        # output: Variable('x'), Application(M, N), Abstraction(x, M) using recursion?
        new_string_list = string.split(' ')

        for i in range(len(new_string_list)):
            if new_string_list[i][0] == 'λ':
                variable = Variable(new_string_list[i][1])
                body = LambdaTerm.fromString(new_string_list[i][3:])
                new_string_list[i] = Abstraction(variable, body)
            else:
                new_string_list[i] = Variable(new_string_list[i])

        for i in range(len(new_string_list)-1):
            new_string_list[0] = Application(
                new_string_list[0], new_string_list[1+i])

        output = new_string_list[0]
        return output

    @staticmethod
    def alphaConversion(**kwargs):
        """Change the symbols in your lambda term with new ones.\n
        \n
        The first argument has to be a lambda term and the following arguments should be the symbol you want to replace and the symbol replacing that symbol.\n
        \n
        Example: LambdaTerm.alphaConversion(LambdaTerm=F, symbol='a', replacesymbol='e', symbol2='b', replacesymbol2='f')"""

        keys = list(kwargs)
        values = list(kwargs.values())
        for i in range(1, len(keys), 2):
            LambdaTerm_repr = repr(values[0])
            LambdaTerm_repr = LambdaTerm_repr.replace(
                f"'{values[i]}'", f"'{values[i+1]}'")
            values[0] = eval(LambdaTerm_repr)
        return eval(LambdaTerm_repr)

    def reduce(self):
        """Beta-reduce."""
        # loop/recursie met substitutie functie erop toegepast
        lijst = [self.substitute()]
        while True:
            lijst.append(lijst[-1].substitute())
            if repr(lijst[-2]) == repr(lijst[-1]):
                break
        return lijst[-1]

    def __eq__(self, other):
        """Alpha-equivalence"""
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
        return f"Variable('{self.symbol}')"

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
        return f'Abstraction({repr(self.variable)}, {repr(self.body)})'

    def __str__(self):
        return f'λ{str(self.variable)}.{str(self.body)}'

    def __call__(self, argument):
        return Application(self, argument).reduce()

    def substitute(self, argument='0'):
        if str(argument) != '0':
            self_repr = repr(self.body).replace(
                repr(self.variable), repr(argument))
            return eval(self_repr)
        else:
            return Abstraction(self.variable.substitute(), self.body.substitute())


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
        # (M N): Check type compatibility first, then if M is an abstraction,
        if isinstance(self.function, Abstraction):
            return self.function.substitute(self.argument)
        else:
            return Application(self.function.substitute(), self.argument.substitute())


# Own programming language
# Natural numbers
zero = Abstraction(Variable('s'), Abstraction(Variable('z'), Variable('z')))
I = Abstraction(Variable('x'), Variable('x'))

##########################################################################################################################################
####### CONDITIONALS #######
##########################################################################################################################################

T = LambdaTerm.fromString('λc.λd.c')
F = LambdaTerm.fromString('λa.λb.b')

And = Abstraction(Variable('x'), Abstraction(
    Variable('y'), Application(Application(Variable('x'), Variable('y')), LambdaTerm.alphaConversion(LambdaTerm=F, symbol='a',
                                                                                                     replacesymbol='e', symbol2='b', replacesymbol2='f'))))
Or = Abstraction(Variable('x'), Abstraction(
    Variable('y'), Application(Application(Variable('x'), LambdaTerm.alphaConversion(LambdaTerm=T, symbol='c', replacesymbol='k', symbol2='d', replacesymbol2='l')), Variable('y'))))
negation = Abstraction(Variable('x'), Application(
    Application(Variable('x'), LambdaTerm.alphaConversion(LambdaTerm=F, symbol='a',
                                                          replacesymbol='g', symbol2='b', replacesymbol2='h')), LambdaTerm.alphaConversion(LambdaTerm=T, symbol='c',
                                                                                                                                           replacesymbol='i', symbol2='d', replacesymbol2='j')))
# 0: True, other numbers are false.
conditional_test = Abstraction(Variable('x'), Application(Application(Application(Variable('x'), LambdaTerm.alphaConversion(LambdaTerm=F, symbol='a', replacesymbol='m', symbol2='b', replacesymbol2='n')),
                               LambdaTerm.alphaConversion(LambdaTerm=negation, symbol='x', replacesymbol='o')), LambdaTerm.alphaConversion(LambdaTerm=F, symbol='a', replacesymbol='p', symbol2='b', replacesymbol2='q')))


print(negation(T).reduce() == F)
print(conditional_test(LambdaTerm.fromNumber(1)) == F)


# print(LambdaTerm.fromstring('lx.y q ly.y z')
#      == LambdaTerm.fromstring('x lx.x q'))


# haakjes uitwerken

# text = input()
# diepte = 0
# haakjes = text.count("(")
# print(haakjes)
# for i in range(haakjes):
#     dieptelijst = []
#     for i in range(len(text)):
#         if text[i] == "(":
#             diepte += 1
#         elif text[i] == ")":
#             diepte -= 1
#         dieptelijst.append(diepte)
#     print(dieptelijst)
#     grootste = 0
#     for i in range(len(dieptelijst)):
#         if dieptelijst[i] > grootste:
#             grootste = dieptelijst[i]
#     grootstespot = False
#     grootserange = 0
#     spotlijst = []
#     for i in range(len(dieptelijst)):
#         if dieptelijst[i] == grootste:
#             grootstespot = True
#             spotlijst.append(i)
#         elif dieptelijst[i] != grootste and grootstespot == True:
#             spotlijst.append(i)
#             break
#     print(spotlijst)

#     origineel = ""
#     vervanging = ""
#     for i in range(spotlijst[0], spotlijst[-1]+1):
#         origineel += text[i]
#     print(origineel)
#     vervanging = origineel.lstrip("(").rstrip(")")

#     text = text.replace(origineel, vervanging)
#     print(text)
