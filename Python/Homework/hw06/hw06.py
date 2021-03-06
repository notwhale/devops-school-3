#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
https://projecteuler.net/problem=36

The decimal number, 585 = 1001001001 in binary, is palindromic in both bases.
Find the sum of all numbers, less than one million, which are palindromic in
base 10 and base 2. (Please note that the palindromic number,
in either base, may not include leading zeros.)

Напишите программу, которая решает описанную выше задачу и печатает ответ.
"""

summ = 0
for decimal in range(1, 1000001):
    if str(decimal) == str(decimal)[::-1] and bin(decimal)[2:] == bin(decimal)[-1:1:-1]:
        summ += decimal
print(summ)
