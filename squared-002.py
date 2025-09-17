#!/usr/bin/env python

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

def get_square_geometry(x, y, spacing, square_size):
    #  size = 200
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

# Create a Drawing object
with Drawing() as draw:
    # Set the fill color for the square
    draw.fill_color = Color('blue')
    # Set the stroke color and width for the square's outline
    draw.stroke_color = Color('black')
    draw.stroke_width = 2

    # Define the rectangle coordinates (left, top, right, bottom)
    # For a square, ensure (right - left) equals (bottom - top)
    #  left = 50
    #  top = 50
    #  side_length = 100
    #  right = left + side_length
    #  bottom = top + side_length
    width = 1200
    height = 2000
    spacing = 100
    columns = 4
    lines = 4

    #  for square in columns

    squares = [(x+1, y+1) for x in range(columns) for y in range(lines)]

    square_size = get_square_size(page_size=width, spacing=spacing, columns=columns)

    for square_x, square_y in squares:
        geometry = get_square_geometry(x=square_x, y=square_y, spacing=spacing, square_size=square_size)
        draw.rectangle(**geometry)


    #  draw.rectangle(left=left, top=top, right=right, bottom=bottom)

    # Create an Image object to draw on
    with Image(width=1200, height=2000, background=Color('white')) as image:
        # Apply the drawing instructions to the image
        draw(image)
        # Save the image to a file
        image.save(filename='square.png')

print("Square drawn and saved as 'square.png'")

print(squares)
