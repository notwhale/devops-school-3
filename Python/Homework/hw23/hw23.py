#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Надо написать функцию которая возвращает N-мерный массив с ширинами заданными в аргументе списком из N элементов:
n_arr([2,2])
>> [[“”,“”],[“”,“”]]
n_arr([2,2,2])
>> [[[“”,“”],[“”,“”]], [[“”,“”],[“”,“”]]]
"""


import os, json


def n_arr(args):
    """
    Function returns N-dimensional array with N-length of each nested array.
    """
    result = [""]
    for arg in args:
        result = [result * arg]
    result = result[0]
    with open('result.json', 'w') as f:
        json.dump(result, f)
    with open('result.json') as f:
        result = json.load(f)
    os.remove('result.json')
    return result


if __name__ == "__main__":
    arr = n_arr([2, 2])
    print(arr)
    arr[0][0] = 'X'
    print(arr)
    print()
    arr = n_arr([2, 2, 2])
    print(arr)
    arr[0][0][0] = 'X'
    print(arr)
