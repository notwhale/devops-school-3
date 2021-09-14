#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Написать функцию-генератор, которая объединяет два отсортированных итератора.
Результирующий итератор должен содержать последовательность в которой содержаться все элементы из каждой коллекции, в упорядоченном виде.

list(merge((x for x in range(1,4)),(x for x in range(2,5)))) == [1,2,2,3,3,4]
"""


from itertools import count, islice


def merge(iter_a, iter_b, limiter=20):
    """
    A generator which joins two sorted iterators.
    """
    iter_a = islice(iter_a, 0, limiter)
    iter_b = islice(iter_b, 0, limiter)
    list_ab = []
    while True:
        try:
            a = next(iter_a)
            list_ab.append(a)
        except StopIteration:
            break
    while True:
        try:
            b = next(iter_b)
            list_ab.append(b)
        except StopIteration:
            break
    list_ab.sort()
    for x in list_ab:
        yield x

if __name__ == "__main__":
    print(list(merge((x for x in range(1, 4)), (x for x in range(2, 5)))))
    # examples with count
    print()
    print(list(merge((x for x in range(1, 4)), count(1))))
    print(list(merge(count(1), (x for x in range(2, 5)))))
    print(list(merge(count(1), count(1))))
    print(list(merge((x for x in range(1, 25)), (x for x in range(2, 25, 6)))))
    #samples from unittest
    print(list(merge((x for x in range(0)), (y for y in range(0)))))
    print(list(merge((x for x in range(1,4)),(x for x in range(2,5)))))
    print(list(merge((x for x in range(11, 25, 3) if not x), (x for x in range(13, 24, 2)))))
    print(list(merge((a for a in range(20)), (b for b in range(10)))))
