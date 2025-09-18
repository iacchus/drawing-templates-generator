#!/usr/bin/env python

import glob

import click

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

@click.group(epilog="gen")
def template_generator():
    pass

width = 1200
height = 2000
resolution = 288
spacing = 11
columns = 4

filename_prefix = "square"
filename_extension = "png"

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

def get_max_lines(page_height, spacing, square_size):
    page_height_without_outer_margins = page_height - (spacing*2)

    count = 0
    total_size = 0

    while total_size < page_height_without_outer_margins:
        count += 1
        total_size = (count * square_size) + ((count - 1) * spacing)

    return count - 1

#  with Drawing() as draw:
#      draw.fill_color = fill_color
#      draw.stroke_color = stroke_color
#      draw.stroke_width = stroke_width
#
#      square_size = get_square_size(page_size=width, spacing=spacing, columns=columns)
#
#      lines = get_max_lines(page_height=height, spacing=spacing, square_size=square_size)
#
#      squares = [(x+1, y+1) for x in range(columns) for y in range(lines)]
#
#      for square_x, square_y in squares:
#          geometry = get_square_geometry(x=square_x, y=square_y, spacing=spacing, square_size=square_size)
#          draw.rectangle(**geometry)
#
#
#      with Image(width=width, height=height, background=background) as image:
#          draw(image)
#
#          filename = create_filename(prefix=filename_prefix, extension=filename_extension)
#          image.save(filename=filename)
#          #  image.save(filename='square.png')

def draw_and_write(shape="square", format="img"):
    with Drawing() as draw:
        draw.fill_color = fill_color
        draw.stroke_color = stroke_color
        draw.stroke_width = stroke_width

        square_size = get_square_size(page_size=width, spacing=spacing, columns=columns)

        lines = get_max_lines(page_height=height, spacing=spacing, square_size=square_size)

        squares = [(x+1, y+1) for x in range(columns) for y in range(lines)]

        if shape == "square":
            for square_x, square_y in squares:
                geometry = get_square_geometry(x=square_x, y=square_y, spacing=spacing, square_size=square_size)
                draw.rectangle(**geometry)
        elif shape == "circle":

            for square_x, square_y in squares:
                geometry = get_circle_geometry(x=square_x, y=square_y, spacing=spacing, square_size=square_size)
                draw.circle(**geometry) # origin, perimeter

        with Image(width=width,
                   height=height,
                   background=background,
                   resolution=resolution) as image:
            draw(image)

            filename = create_filename(prefix=filename_prefix, extension=filename_extension)
            image.save(filename=filename)
            #  image.save(filename='square.png')
width_option = click.option("-w", "--width", type=int, default=1200)
height_option = click.option("-h", "--height", type=int, default=2000)
spacing_option = click.option("-s", "--spacing", type=int, default=33)
columns_option = click.option("-c", "--columns", type=int, default= 4)
page_option = click.option("-p", "--page", type=str, default="a4")  # "a4" etc... type is Choice
dpi_option = click.option("-d", "--dpi", type=int, default=288)  # 72, 288 etc
shape_option = click.option("-x", "--shape", type=click.Choice(["square", "circle"], case_sensitive=False))  # square or circle
#  format_option = click.option()  # img or pdf

@template_generator.command(epilog="generate image")
@width_option
@height_option
@spacing_option
@columns_option
@page_option
@dpi_option
@shape_option
def img():
    filename_prefix = "square"
    filename_extension = "png"

@template_generator.command(epilog="generate pdf")
@page_option
@spacing_option
@columns_option
@dpi_option
@shape_option
def pdf():
    filename_prefix = "square"
    filename_extension = "pdf"

#  print("Squared template drawn and saved as", filename)

