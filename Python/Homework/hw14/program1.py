#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Создать сотрудника Mary, пользуясь классом
Employee и перенести его в другую программу,
используя модуль Pickle и файловую систему.
Узнать про + и - модуля Pickle.
"""

import pickle, empmod as emp
employee_mary = emp.Employee(123, 'Mary', 'HR', 'Manager')
with open('employee.pkl', 'wb') as f:
    pickle.dump(employee_mary, f)
