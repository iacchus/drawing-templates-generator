#!/usr/bin/env python

import glob
from ntpath import isfile
import os

import click

from wand.image import Image
from wand.image import PAPERSIZE_MAP
from wand.drawing import Drawing
from wand.color import Color

#  @click.group(epilog="gen")
#  def template_generator():
#      pass

#  width = 1200
#  height = 2000
#  resolution = 288
#  spacing = 11
#  columns = 4

#  filename_prefix = "square"
#  filename_extension = "png"

#  stroke_width = 2
#  fill_color = Color("white")
#  stroke_color = Color("black")
#  background = Color("white")

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


def draw_and_write(width, height, spacing, columns, resolution, shape,
                   file_format, stroke_width, stroke_color, fill_color,
                   background_color):

    with Drawing() as draw:
        draw.fill_color = fill_color
        draw.stroke_color = stroke_color
        draw.stroke_width = stroke_width

        square_size = get_square_size(page_size=width, spacing=spacing, columns=columns)

        lines = get_max_lines(page_height=height, spacing=spacing, square_size=square_size)

        squares = [(x+1, y+1) for x in range(columns) for y in range(lines)]

        if shape == "square":
            for square_x, square_y in squares:
                geometry = get_square_geometry(x=square_x,
                                               y=square_y,
                                               spacing=spacing,
                                               square_size=square_size)
                draw.rectangle(**geometry)

        elif shape == "circle":
            for square_x, square_y in squares:
                geometry = get_circle_geometry(x=square_x,
                                               y=square_y,
                                               spacing=spacing,
                                               square_size=square_size)
                draw.circle(**geometry) # origin, perimeter

        with Image(width=width,
                   height=height,
                   background=background_color,
                   resolution=resolution) as image:
            draw(image)

            filename = create_filename(prefix=shape, extension=file_format)

            image.save(filename=filename)
            if os.path.isfile(filename):
                print("Created", file_format, "file", filename)
            else:
                print("Error creating", filename)
            #  image.save(filename='square.png')


width_option = click.option("--width", type=int, default=1200)
height_option = click.option("--height", type=int, default=2000)
spacing_option = click.option("--spacing", type=int, default=33)
columns_option = click.option("--columns", type=int, default=4)
page_option = click.option("--page", type=str, default="a4")  # "a4" etc... type is Choice
dpi_option = click.option("--dpi", type=int, default=288)  # 72, 288 etc
#  shape_option = click.option("--shape", type=click.Choice(["square", "circle"], case_sensitive=False))  # square or circle
square_option = click.option("--square", "shape", is_flag=True, flag_value="square", default="square")
circle_option = click.option("--circle", "shape", is_flag=True, flag_value="circle")
png_option = click.option("--png", "file_format", is_flag=True, flag_value="png", default="png")
pdf_option = click.option("--pdf", "file_format", is_flag=True, flag_value="pdf")
fill_color_option = click.option("--fill-color", type=str, default="white")
stroke_color_option = click.option("--stroke-color", type=str, default="black")
background_color_option = click.option("--background-color", type=str, default="white")
stroke_width_option = click.option("--stroke-width", type=int, default=2)
#  format_option = click.option()  # img or pdf

#  @template_generator.command(epilog="generate image")

@click.command(epilog="generate image")
@width_option
@height_option
@spacing_option
@columns_option
@page_option
@dpi_option
@square_option
@circle_option
@png_option
@pdf_option
@stroke_width_option
@stroke_color_option
@fill_color_option
@background_color_option
def generate_template(width, height, spacing, columns, page, dpi, shape,
                      file_format, stroke_width, stroke_color, fill_color,
                      background_color):
    resolution_factor = dpi / 72

    if file_format == "pdf":
        page_w, page_h = PAPERSIZE_MAP[page]  # this size is for 72dpi
        width = int(page_w * resolution_factor)
        height = int(page_h * resolution_factor)

    draw_and_write(width=width,
                   height=height,
                   spacing=spacing,
                   columns=columns,
                   resolution=dpi,
                   shape=shape,
                   file_format=file_format,
                   stroke_width=stroke_width,
                   stroke_color=Color(stroke_color),
                   fill_color=Color(fill_color),
                   background_color=Color(background_color))


generate_template()
