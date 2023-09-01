#!/usr/bin/env python

import random
import string


def rand_name(min: int = 5, max: int = 20) -> str:
    return "".join(
        random.choices(string.ascii_letters)
        + (
            random.choices(
                string.ascii_letters + string.digits, k=random.randint(min, max)
            )
        )
    )


# create a list of 10 random strings of length 5-20
names = [rand_name() for _ in range(10)]
print(names)

# create a list of the string lengths next to the strings and sort
# as the length is the 2nd element we need to use the key parameter
lengths = sorted([(name, len(name)) for name in names], key=lambda x: x[1])
print(lengths)

# double loop
for x in range(3):
    for y in range(5, 8):
        print(f"{x} * {y} = {x*y}")

# list comprehension
print([f"{x} * {y} = {x*y}" for x in range(3) for y in range(5, 8)])
