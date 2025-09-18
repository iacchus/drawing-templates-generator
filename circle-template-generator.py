#!/usr/bin/env python

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

#  def get_square_geometry(x, y, spacing, square_size):
#      left = spacing * x + (x-1)*square_size
#      top = spacing * y + (y-1)*square_size
#      right = spacing * x + (x)*square_size
#      bottom = spacing * y + (y)*square_size
#
#      geometry = dict(
#              left=left,
#              top=top,
#              right=right,
#              bottom=bottom
#              )
#
#      return geometry

def get_circle_geometry(x, y, spacing, square_size):
    left = spacing * x + (x-1)*square_size
    top = spacing * y + (y-1)*square_size
    #  right = spacing * x + (x)*square_size
    #  bottom = spacing * y + (y)*square_size

    origin_x = left + (square_size/2)
    origin_y = top + (square_size/2)

    perimeter_x = left + (square_size/2)
    perimeter_y = top

    geometry = dict(
            origin=(origin_x, origin_y),
            perimeter=(perimeter_x, perimeter_y)
            )

    return geometry

def get_square_size(page_size, spacing, columns):
    outer_margin = spacing * 2
    intermediary_total_padding = ((columns-1) * spacing)
    spacing_total_size = outer_margin + intermediary_total_padding
    square_total_size = page_size - spacing_total_size
    square_size = square_total_size / columns

    return square_size

#  def get_circle_size(page_size, spacing, columns):
#      outer_margin = spacing * 2
#      intermediary_total_padding = ((columns-1) * spacing)
#      spacing_total_size = outer_margin + intermediary_total_padding
#      square_total_size = page_size - spacing_total_size
#      square_size = square_total_size / columns
#
#      return square_size

def get_max_lines(page_height, spacing, square_size):
    page_height_without_outer_margins = page_height - (spacing*2)

    count = 0
    total_size = 0

    while total_size < page_height_without_outer_margins:
        count += 1
        total_size = (count * square_size) + ((count - 1) * spacing)

    return count - 1

with Drawing() as draw:
    draw.fill_color = Color('white')
    draw.stroke_color = Color('black')
    draw.stroke_width = 2

    width = 1200
    height = 2000
    spacing = 33
    columns = 6

    square_size = get_square_size(page_size=width, spacing=spacing, columns=columns)

    lines = get_max_lines(page_height=height, spacing=spacing, square_size=square_size)

    squares = [(x+1, y+1) for x in range(columns) for y in range(lines)]

    for square_x, square_y in squares:
        geometry = get_circle_geometry(x=square_x, y=square_y, spacing=spacing, square_size=square_size)
        draw.circle(**geometry) # origin, perimeter


    with Image(width=1200, height=2000, background=Color('white')) as image:
        draw(image)
        image.save(filename='circle.png')

print("Squared template drawn and saved as 'circle.png'")

