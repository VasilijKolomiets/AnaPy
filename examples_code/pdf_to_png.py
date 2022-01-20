# -*- coding: utf-8 -*-
"""
Created on Thu Dec  9 19:47:53 2021

@author: Vasil
"""
import fitz
import glob, sys

# To get better resolution
zoom_x = 2.0  # horizontal zoom
zoom_y = 2.0  # vertical zoom
mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

path = 'pdfs/'
all_files = glob.glob(path + "*.pdf")
print
for filename in all_files:
    doc = fitz.open(filename)  # open document
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        pix.save("data_out/page-%i.png" % page.number)  # store image as a PNG


all_files = glob.glob(path + "*.pdf")
print(all_files)



"""
import fitz

pdffile = "infile.pdf"
doc = fitz.open(pdffile)
page = doc.loadPage(0)  # number of page
pix = page.get_pixmap()
output = "outfile.png"
pix.save(output)
"""
