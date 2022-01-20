# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 18:39:52 2021

@author: Vasil
"""

from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (300, 40))
draw = ImageDraw.Draw(img)
str = 'Привет\nПривет'
font = ImageFont.truetype('arial.ttf', 12, encoding='UTF-8')  #   'monocondensedc.ttf'
# draw.text((10, 10), str) -- ошибка
draw.text((10, 1), str, font=font)
img.show()
img.save('test.jpg')
