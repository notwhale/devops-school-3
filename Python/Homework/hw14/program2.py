#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Создать сотрудника Mary, пользуясь классом
Employee и перенести его в другую программу,
используя модуль Pickle и файловую систему.
Узнать про + и - модуля Pickle.
"""

import pickle, empmod
with open('employee.pkl', 'rb') as f:
    employee_mary = pickle.load(f)
print(employee_mary.info())
