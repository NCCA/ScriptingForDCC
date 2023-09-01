#!/usr/bin/env python

from functools import reduce

a=list(range(10))
b=[x*2 for x in a]
print("map using list comprehension")
print(f"{a}\n{b}")

print("filter using list comprehension")
c=[x for x in a if x%2==0]
print(f"{a}\n{c}")

print("reduce using list comprehension (not recommended)")
total = sum([a[0]] + [x for x in a[1:]])
print(f"{a}\n{total}")