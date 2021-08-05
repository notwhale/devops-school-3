#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Встроенная функция input позволяет ожидать и возвращать данные из стандартного
ввода ввиде строки (весь введенный пользователем текст до нажатия им enter).
Используя данную функцию, напишите программу, которая:

    1. После запуска предлагает пользователю ввести неотрицательные целые числа,
    разделенные через пробел и ожидает ввода от пользователя.
    2. Находит наименьшее положительное число, не входящее в данный пользователем
    список чисел и печатает его.


    Например:

        -> 2 1 8 4 2 3 5 7 10 18 82 2
        6
"""

input_list = list(map(int, input('Введите неотрицательные числа, разделенные пробелами: ').strip().split()))
input_list.sort()
for digit in range (input_list[0], len(input_list) + 2):
    if digit not in input_list:
        print(digit)
        break