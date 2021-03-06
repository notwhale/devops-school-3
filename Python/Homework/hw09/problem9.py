#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Решить несколько задач из projecteuler.net

Решения должны быть максимально лаконичными, и использовать list comprehensions.

problem6 - list comprehension : one line
problem9 - list comprehension : one line
problem40 - list comprehension
problem48 - list comprehension : one line

Special Pythagorean triplet
Problem 9
A Pythagorean triplet is a set of three natural numbers, a < b < c, for which, a^2 + b^2 = c^2
For example, 32 + 42 = 9 + 16 = 25 = 52.
There exists exactly one Pythagorean triplet for which a + b + c = 1000.
Find the product abc.
"""

print(*[(a * b * (1000 - a - b)) for a in range(1, 1000 // 3 + 1) for b in range(a + 1, 1000 // 2 + 1) if a < b < (1000 - a - b) if a ** 2 + b ** 2 == (1000 - a - b) ** 2])
