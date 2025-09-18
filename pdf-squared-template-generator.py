#!/usr/bin/env python

import glob

from wand.image import Image
from wand.image import PAPERSIZE_MAP
from wand.drawing import Drawing
from wand.color import Color

page_w, page_h = PAPERSIZE_MAP["a4"]  # this size is for 72dpi
width, height = (page_w * 4, page_h * 4)

resolution = 288
spacing = 11
columns = 4

filename_prefix = "square"
filename_extension = "pdf"

stroke_width = 2
fill_color = Color("white")
stroke_color = Color("black")
background = Color("white")

def get_filename_number(filename):
    filename_without_extension = filename.split(".")[0]
    number = filename_without_extension.split("-")[1]

    return number if number.isdecimal() else -1

def create_filename(prefix, extension):
    filename_wildcard = f"{prefix}-*.{extension}"
    files = glob.glob(filename_wildcard)
    numbers = [int(get_filename_number(filename)) for filename in files]
    next_number = 0
    if numbers:
        next_number = max(numbers) + 1
    next_number_str = str(next_number).zfill(3)
    filename = f"{prefix}-{next_number_str}.{extension}"
    return filename

def get_square_geometry(x, y, spacing, square_size):
    left = spacing * x + (x-1)*square_size
    top = spacing * y + (y-1)*square_size
    right = spacing * x + (x)*square_size
    bottom = spacing * y + (y)*square_size

    geometry = dict(
            left=left,
            top=top,
            right=right,
            bottom=bottom
            )

    return geometry

def get_square_size(page_size, spacing, columns):
    outer_margin = spacing * 2
    intermediary_total_padding = ((columns-1) * spacing)
    spacing_total_size = outer_margin + intermediary_total_padding
    square_total_size = page_size - spacing_total_size
    square_size = square_total_size / columns

    return square_size

def get_max_lines(page_height, spacing, square_size):
    page_height_without_outer_margins = page_height - (spacing*2)

    count = 0
    total_size = 0

    while total_size < page_height_without_outer_margins:
        count += 1
        total_size = (count * square_size) + ((count - 1) * spacing)

    return count - 1

with Drawing() as draw:
    draw.fill_color = fill_color
    draw.stroke_color = stroke_color
    draw.stroke_width = stroke_width
    #  draw.fill_color = Color('white')
    #  draw.stroke_color = Color('black')
    #  draw.stroke_width = 1

    #  width = 1200
    #  height = 2000
    #  spacing = 11
    #  columns = 4

    square_size = get_square_size(page_size=width, spacing=spacing, columns=columns)

    lines = get_max_lines(page_height=height, spacing=spacing, square_size=square_size)

    squares = [(x+1, y+1) for x in range(columns) for y in range(lines)]

    for square_x, square_y in squares:
        geometry = get_square_geometry(x=square_x, y=square_y, spacing=spacing, square_size=square_size)
        draw.rectangle(**geometry)


    with Image(width=width,
               height=height,
               background=background,
               resolution=resolution) as image:
        draw(image)

        filename = create_filename(prefix=filename_prefix, extension=filename_extension)
        image.save(filename=filename)
        #  image.save(filename='square.png')

print("Squared template drawn and saved as", filename)

