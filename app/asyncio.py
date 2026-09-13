def greet_named(name):
    print(f"Hello, {name} weclcome to my python tutorial")

greet_named("Omprakash Chaudhary")

def outer_function():
    print("This is the outer function")

    def inner_function():
        print("This is the inner function")

    print("Outer function called again")

    inner_function()
    print("Outer function will be called after inner function.")

outer_function()

# Lambda (Anonymous function)
# In Python, a lambda function is a small, anonymous function that is defined without a name. While normal functions are created using the def keyword, lambda functions are built on the fly using the lambda keyword

square = lambda x: x**2
print(square)

add = lambda a, b: a + b
print(f"sum of a , b : {add(1,2)}")

# recursion
def adds(a, b):
    """This function multiplies two numbers"""
    return a * b

print(adds(2, 5))
print(adds.__doc__)


# factorial
def factorial(n):
    if n == 1 or n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(0))

def factorial_sum(n):
    return factorial(n) + n

def name(a: str, b: str):
    print(f"my{b} name is nothing {a}")


def name():
    print("my name is something")

