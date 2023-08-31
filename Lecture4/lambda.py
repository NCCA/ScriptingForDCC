#!/usr/bin/env python


def double(x):
    """This function multiplies its argument by two."""
    return x * 2


a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(a)

# This code applies the double function to each element in the list a and prints the resulting list.
new_list = []
for i in a:
    new_list.append(double(i))
print(new_list)

# This code applies the double_lambda function to each element in the list a and prints the resulting list.
# The map() function applies a given function to each element of an iterable and returns a map object
# # which can be converted to a list.

double_lambda = lambda x: x * 2
map_list = list(map(double_lambda, a))
print(map_list)
# Note we can also use an existing function in map as well as a lambda

func_list = list(map(double, a))
print(func_list)

# or inline the lambda
print(list(map(lambda x: x * 2, a)))
