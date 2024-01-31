# Lambda Calculus in Python

> [!NOTE]
> This code is not fully completed (yet). To see what is missing, see the chapter 'Discussion' in "Lambda Calculus.pdf". 


## Why?

The motivation behind this code is for people to learn about lambda calculus and functional programming and play with it, with only a basic background in Python. Functional programming is considered an advanced topic in computer science, but with our code, we hope that the basic concepts behind it will be accessible to curious beginners. For more information about the basics of lambda calculus and its rules, we refer you to the file "Lambda Calculus.pdf" which can be found in this repository.

## What can you do with our code?
We have implemented several methods from lambda calculus into Python, which we list below. We will explain how to use them in the next chapter.
* Define lambda terms: variables, applications and abstractions.
* fromString: create a lambda term from a string
* alphaConversion: convert a variable letter
* reduce: this method constantly subsitutes terms inside lambda terms to _bèta-reduce_ the lambda term.
* \_\_eq\_\_ (alpha-equivalence): this method, which can be called by using the '=='-symbol between lambda terms, checks whether two lambda terms are alpha-equivalent to each other.
* Arithmetic operations: we implemented basic arithmetic operations using the Church encoding for natural numbers and addition and multiplication between them. For the definition of the Church encoding for natural numbers, we refer you to "Lambda Calculus.pdf".
  * successor: returns the successor of the natural number.
  * fromNumber: converts a natural number to a lambda term.
  * toNumber: converts a natural number as a lambda term to a natural number.
* Conditionals: basic conditionals such as True, False, AND, OR, negation, conditional test, recursion, and recursive sum. For these definitions, we refer you to our Python code or "Lambda Calculus.pdf". It's also possible to define simple to write simple conditional statements such as "If P then A, else B". We note however that recursion and recursive sum are not fully functional (yet) since we haven't fully resolved all problems in this code yet. For more information, see the chapter 'Discussion' in "Lambda Calculus.pdf". 

## How can you use it?
For our full breakdown and explanation of the code and lambda calculus, we refer you to the file "Lambda Calculus.pdf". Here, we provide several small examples of how you can use our code.

### Creating Lambda Terms
**Variables**
```Python
# Put in a symbol for your variable as argument.
x = Variable('x')
```

**Abstractions**
```Python
# Put in a variable as first argument, and a lambda term (variable, application or abstraction) as the second argument.
# identity = λx.x
identity = Abstraction(Variable('x'), Variable('x'))
```
We also made a special function for abstractions: you can instantly apply a lambda term to an abstraction by treating the abstraction as a function:
```Python
identity = Abstraction(Variable('x'), Variable('x'))
y = Variable('y')

print(identity(y))
>>> 'y'
```

**Applications**
```Python
# Put in a lambda term as first argument, and another lambda term as the second argument.
# A = (λx.x y) = y
A = Application(identity, Variable('y'))
```

### Basic Functions
#### fromString
This method converts a string into a lambda term. The rules for this to work in our code is as follows: 
1. abstractions should be written with 'λ' (one may change this with any other letter such as 'l')
2. applications should be written within parentheses. One may define order priority in this way (which application goes first, second, etc.).
This method is a static method.
```Python
successor = LambdaTerm.fromString('λw.λy.λx.(y ((w y) x))')

zero = LambdaTerm.fromString('λs.λf.f')
```

#### alphaConversion
This method is a static method.
```Python
# The first argument has to be a lambda term and the following arguments should be the symbols you want to replace and the symbols replacing that symbol in alternating fashion.
# F = λa.λb.b; new_F = λe.λf.f

F = LambdaTerm.fromString('λa.λb.b')
new_F = LambdaTerm.alphaConversion(LambdaTerm=F, symbol='a', replacesymbol='e', symbol2='b', replacesymbol2='f')

print(new_F)
>>> 'λe.λf.f'
```

#### reduce
Applies the substitute() method on the lambda terms continually, until the subtituted lambda term is no different from the previous lambda term. This method provides the same functionality as bèta-reduction.
```Python
# Applying the successor function on 1 gives us 2: (successor 1) = 2
one = LambdaTerm.fromString('λy.λx.(y x)')

print(Application(successor, one).reduce())
>>> 'λy.λx.(y (y x))'
```
#### \_\_eq\_\_
Looks if two lambda terms are the same.
```Python
# Applying the successor function on 1 gives us 2: (successor 1) = 2

one = LambdaTerm.fromString('λy.λx.(y x)')
two = LambdaTerm.fromString('λy.λx.(y (y x))')

print(two == Application(successor, one).reduce())
>>> True
```

### Basic Arithmetic
#### successor
This method applies the successor function on a number (as a lambda term or as a natural number). This method is a static method. An example:
If we apply the successor function on 2, we get:

(λw.λy.λx.(y ((w y) x)) λs.(λz.(s (s z))))  
λy.λx.(y ((λs.(λz.(s (s z))) y) x))  
λy.λx.(y (λz.(y (y z))) x))  
λy.λx.(y (y (y x))) = 3  

In Python, we can write this as:
```Python
print(LambdaTerm.successor(2))
>>> 'λy.λx.(y (y (y x)))'

two = LambdaTerm.fromString('λy.λx.(y (y x))')
print(LambdaTerm.successor(two))
>>> 'λy.λx.(y (y (y x)))'
```
#### Addition and Multiplication
Addition and multiplication defined for Church encoding of natural numbers.
```Python
print(one + two)
>>> 'λy.λx.(y (y (y x)))'

print(one * two)
>>> 'λy.λx.(y (y x))'
```

#### fromNumber
This method is a static method.
```Python
print(LambdaTerm.fromNumber(2))
>>> 'λy.λx.(y (y x))'
```

#### toNumber
This method is a static method.
```Python
print(LambdaTerm.toNumber(two))
>>> 2
```

### Basic Conditionals

We can define basic conditionals as:  

T = λa.(λb.b)  
F = λc.(λd.c)  
AND =  λx.(λy.((x y) F))  
OR = λx.(λy.((x T) y)) 

where T stands for True and F for False.

#### negation
The negation operator ¬ gives us the opposite conditional. So when we apply it to True we get False, and the same goes for the other direction. We will provide an example of ¬True = False. In lambda calculus we can define the negation operator as: λx.((x F) T ). So, if we apply this to True, we get:

(λx.((x λa.(λb.b)) λc.(λd.c)) λe.(λf.e))  
(((λe.(λf.e) λa.(λb.b)) λc.(λd.c))  
(λf.(λa.(λb.b)) λc.(λd.c))  
λa.(λb.b)  
F 

In our code, it would look like this:
```Python
negation = LambdaTerm.fromString(f'λx.((x {F}) {T} )')

print(negation(T))
>>> 'λa.λb.b'
```

#### Conditional test
The conditional test applied to zero gives us True and for any other number, gives us False. It appears to be useful to have such a function (Python also has this). We can define it as: conditional_test = λx.(((x F) ¬) F). For example, if we apply this function to 0, we get

(λx.(((x F) ¬) F) 0)  
(((0 F) ¬) F)  
((I ¬) F)  
(¬ F)  
T

where I is the identity function. Now, (0 F) = I because:

(λs.(λz.z) F)  
λz.z  
I  

Now, if we apply it to any integer N not equal to 0, we get

(λx.(((x F) ¬) F) 0)  
(((N F) ¬) F)  
((F ¬) F)  
(I F)  
F

where we used the facts that (N F) = F, and (F ¬) = I. We leave it as an exercise for the reader to confirm this.

Implemented in Python gives us the code below. Note that we had to manually change the variable names for False inside conditional_test. This issue has been brought up earlier.
```Python
T = LambdaTerm.fromString('λc.λd.c')
F = LambdaTerm.fromString('λa.λb.b')
negation = LambdaTerm.fromString(f'λx.((x {F}) {T} )')
conditional_test = LambdaTerm.fromString(
    f'λi.(((i λg.λh.h) {negation}) λe.λf.f)')
zero = LambdaTerm.fromString('λs.λf.f')
one = LambdaTerm.successor(zero)

print(conditional_test(zero))
>>> 'λc.λd.c'

print(conditional_test(one))
>>> 'λe.λf.f'
```

#### Conditional statements
We can also construct basic conditional statements such as: "If P then A, else B", where P, A, and B are statements. This is done by means of application: ((P A) B). This is because, if P is true, then by definition of T, it will return the first argument so A. If P is false, then by definition, it returns the second argument so B. An example in Python is shown below. Again, we had to change the variable names.
```Python
x = Variable('x')
y = Variable('y')


T = LambdaTerm.fromString('λc.λd.c')
F = LambdaTerm.fromString('λa.λb.b')
negation = LambdaTerm.fromString(f'λx.((x {F}) {T} )')
conditional_test = LambdaTerm.fromString(
    f'λi.(((i λg.λh.h) {negation}) λe.λf.f)')
zero = LambdaTerm.fromString('λs.λf.f')
one = LambdaTerm.successor(zero)

# If 0 then x, else y; 0 is True, so we get back x
statement = LambdaTerm.fromString(f'(({conditional_test(zero)} {x}) {y})')

print(statement.reduce())
>>> 'x'

# If 1 then x, else y; 1 is False so we get back y
statement = LambdaTerm.fromString(f'(({conditional_test(one)} {x}) {y})')

print(statement.reduce())
>>> 'y'
```



