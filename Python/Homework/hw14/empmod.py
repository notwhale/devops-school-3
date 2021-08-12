#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Employee:
    def __init__(self, employee_id, name, department, job_title):
        self.employee_id = employee_id
        self.name = name
        self.department = department
        self.job_title = job_title

    def set_name(self, name):
        self.name = name

    def set_employee_id(self, employee_id):
        self.employee_id = employee_id

    def set_department (self, department):
        self.department = department

    def set_job_title (self, job_title):
        self.job_title = job_title

    def get_name(self):
        return self.name

    def get_employoee_id(self):
        return self.employee_id

    def get_department(self):
        return self.department

    def get_job_title(self):
        return self.job_title

    def __str__(self):
        return f'{self.name} (id={self.employee_id}) is {self.job_title} from {self.department}'

    info = __str__
