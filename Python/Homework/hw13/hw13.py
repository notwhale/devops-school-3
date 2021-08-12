#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Напишите функцию, которая переводит значения показаний
температуры из Цельсия в Фаренгейт и наоборот.
"""

def temp_conv(temp, prec=1, form='fulllist'):
    """
    Converts the temperature from Celsius to Fahrinheit and viсe versa.
    Parameters:
        prec - precision (default=1)
        form - output data format (default='fulllist'):
            fulllist - a list of a numeric value with units of measurement
            valueonly - a numeric value only
            fullstring - a numeric value with units of measurement as a formatted string
    """
    import re
    if temp:
        temp_regexp = re.search(r'^\s*(?P<temp_value>[+-]?(?P<temp_value_abs>([0-9]+([.,][0-9]*)?|[.,][0-9]+)))\s*(?P<temp_scale>[cCfF]{1})?.*$', temp)
        if temp_regexp:
            if temp_regexp.group('temp_value') and temp_regexp.group('temp_value_abs'):
                temp_value = float(temp_regexp.group('temp_value').replace(',', '.'))
                temp_scale = temp_regexp.group('temp_scale').upper() if temp_regexp.group('temp_scale') else 'C'
                if temp_scale == 'C':
                    res_value = round(temp_value * (9 / 5) + 32, prec)
                    res_scale = '°F'
                elif temp_scale == 'F':
                    res_value = round((temp_value - 32) * (5 / 9), prec)
                    res_scale = '°C'
                if form == 'fulllist':
                    result = [ res_value, res_scale ]
                elif form == 'valueonly':
                    result = res_value
                elif form == 'fullstring':
                    result = f'{res_value} {res_scale}'
                return result

if __name__ == '__main__':
    temp_input_list = ['0', '.5', '36.6', '-15,5', '13.', '.0f', '60,1F', '-49.6 F', '37.c', '-23.33C', '-1,1 C']
    print('Examples: ', *['\t = '.join(_) for _ in zip(temp_input_list, list(' '.join(map(str, _)) for _ in map(temp_conv, temp_input_list)))], sep='\n', end='\n\n')

    temp_input = input('Enter the temperature: ')
    for _ in ('fulllist', 'valueonly', 'fullstring'):
        print(f"form='{_}': {temp_conv(temp_input, prec=2, form=_)}")
