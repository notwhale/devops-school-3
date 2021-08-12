#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Написать функцию Фиббоначи fib(n), которая вычисляет
элементы последовательности Фиббоначи:
1 1 2 3 5 8 13 21 34 55 .......
"""

def fib(n):
    """
    Return n'th element of the fibbonaci(n)
    """
    fib_list = []
    a, b = 1, 1
    for _ in range(n):
        fib_list.append(a)
        a, b = b, a + b
    return fib_list[n - 1]

if __name__ == "__main__":
    elem = int(input('Введите аргумент: '))
    print(fib(elem))
