#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Написать скрипт, который будет создавать миниатюры фотографий.
Объем полученого файла должен передаваться как параметр.
"""

import os
from optparse import OptionParser
from PIL import Image

def parse_options():
    parser = OptionParser(usage="usage: %prog [options] arg1 arg2")
    parser.add_option("-s", "--scale", type="int", dest="scale", default=10, help="scale as a percentage of the original size, [default: %default]")
    parser.add_option("-q", "--quality",type="int", dest="quality", default=95, help="quality of the output image thumbnail, [default: %default]")
    return parser.parse_args()

def get_files(ext):
    return [ file for file in os.listdir('.') if os.path.isfile(file) and file.lower().endswith(ext) and not file.lower().startswith('thumbnail_') ]

def thumbnail(filename, scale, quality):
    img = Image.open(filename)
    width, height = img.size
    width = width * scale // 100
    height = height * scale // 100
    new_size = width, height
    img.thumbnail(size=new_size)
    img.save('thumbnail_' + filename, optimized=True, quality=quality)
    return print(f'Thumbnail for file "{filename}" has been created.')

if __name__ == "__main__":
    (options, args) = parse_options()
    images = get_files(('jpg', 'jpeg', 'png'))
    if images:
        for image in images:
            thumbnail(image, scale=options.scale, quality=options.quality)
