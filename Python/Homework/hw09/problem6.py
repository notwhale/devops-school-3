#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Решить несколько задач из projecteuler.net

Решения должны быть максимально лаконичными, и использовать list comprehensions.

problem6 - list comprehension : one line
problem9 - list comprehension : one line
problem40 - list comprehension
problem48 - list comprehension : one line

Sum square difference
Problem 6
The sum of the squares of the first ten natural numbers is, 1^2 + 2^2 +  ... + 10^2 = 385
The square of the sum of the first ten natural numbers is, (1 + 2 + ... + 10)^2 = 3025
Hence the difference between the sum of the squares of the first ten natural numbers and the square of the sum is 3025 - 385 = 2640.
Find the difference between the sum of the squares of the first one hundred natural numbers and the square of the sum.
"""

print(sum([_ for _ in range(1, 101)]) ** 2 - sum(map(lambda x: x**2, [_ for _ in range(1, 101)])))
