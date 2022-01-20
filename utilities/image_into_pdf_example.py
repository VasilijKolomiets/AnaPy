# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 13:00:44 2021

@author: manager
"""
import fitz   # <-- PyMuPDF
from PIL import Image, ImageDraw, ImageFont

# create an image
out = Image.new("RGB", (226, 34), (255, 255, 255))

# get a font

#  fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
# fnt = ImageFont.truetype("Roboto-Regular.ttf", 12, encoding='UTF-8')
fnt = ImageFont.load_default()

# get a drawing context
d = ImageDraw.Draw(out)

# draw multiline text
d.multiline_text(
    (1, 1),
    "m.Lviv, проспект Chornivola, 40\n kalendar 5sht. po 25".encode('UTF-8'),
    font=fnt, fill=(0, 0, 0))

out.show()
out.save('patern.png')


doc = fitz.open("some.pdf")          # open the PDF
rect = fitz.Rect(5, 25, 226, 34)     # where to put image: use upper left corner

for page in doc:
    page.insertImage(rect, filename="patern.png")

doc.saveIncr()                       # do an incremental save
# The above script is very fast: to sta
