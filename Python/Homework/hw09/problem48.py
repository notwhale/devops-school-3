#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Решить несколько задач из projecteuler.net

Решения должны быть максимально лаконичными, и использовать list comprehensions.

problem6 - list comprehension : one line
problem9 - list comprehension : one line
problem40 - list comprehension
problem48 - list comprehension : one line

Self powers
Problem 48
The series, 1^1 + 2^2 + 3^3 + ... + 10^10 = 10405071317.
Find the last ten digits of the series, 1^1 + 2^2 + 3^3 + ... + 1000^1000.
"""

print(str(sum(_ ** _ for _ in range(1, 1000 + 1)))[-10:])
