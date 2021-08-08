#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Решить несколько задач из projecteuler.net

Решения должны быть максимально лаконичными, и использовать list comprehensions.

problem6 - list comprehension : one line
problem9 - list comprehension : one line
problem40 - list comprehension
problem48 - list comprehension : one line

Champernowne's constant
Problem 40
An irrational decimal fraction is created by concatenating the positive integers: 0.123456789101112131415161718192021...
It can be seen that the 12th digit of the fractional part is 1.
If d_n represents the n_th digit of the fractional part, find the value of the following expression.
d_1 × d_10 × d_100 × d_1000 × d_10000 × d_100000 × d_1000000
"""

from functools import reduce
print(reduce(lambda x, y: x * y, list(map(int, [''.join(map(str, [_ for _ in range(1, d + 1)]))[d - 1] for d in [pow(10, _) for _ in range(7)]]))))
