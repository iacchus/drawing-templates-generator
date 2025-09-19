#!/usr/bin/env python

import glob
import os

import click

from wand.image import Image
from wand.image import PAPERSIZE_MAP
from wand.drawing import Drawing
from wand.color import Color


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

        for square_x, square_y in squares:
            square_data = dict(x=square_x,
                               y=square_y,
                               spacing=spacing,
                               square_size=square_size)

            if shape == "square":
                    geometry = get_square_geometry(**square_data)
                    draw.rectangle(**geometry)

            elif shape == "circle":
                    geometry = get_circle_geometry(**square_data)
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


width_option = click.option("--width",
                            type=int,
                            default=1200,
                            metavar="<int>",
                            show_default=True,
                            help="Width for the generated png image")

height_option = click.option("--height",
                             type=int,
                             default=2000,
                             metavar="<int>",
                             show_default=True,
                             help="Height for the generated png image")

spacing_option = click.option("--spacing",
                              type=int,
                              default=33,
                              metavar="<int>",
                              show_default=True,
                              help="Margin/padding between the shapes, in pixels")

columns_option = click.option("--columns",
                              type=int,
                              default=6,
                              metavar="<int>",
                              show_default=True,
                              help="How many shapes to draw in a line")

page_option = click.option("--page",
                           type=str,
                           default="a4",
                           metavar="<str>",
                           show_default=True,
                           help="Page format for pdf")  # "a4" etc... type is Choice

dpi_option = click.option("--dpi",
                          type=int,
                          default=288,
                          metavar="<int>",
                          show_default=True,
                          help="Resolution for the pdf document")  # 72, 288 etc

square_option = click.option("--square",
                             "shape",
                             is_flag=True,
                             flag_value="square",
                             default="square",
                             show_default=True,
                             help="Use squares as shape")

circle_option = click.option("--circle",
                             "shape",
                             is_flag=True,
                             flag_value="circle",
                             help="Use circles as shape")

png_option = click.option("--png",
                          "file_format",
                          is_flag=True,
                          flag_value="png",
                          default="png",
                          show_default=True,
                          help="Generates a png image")

pdf_option = click.option("--pdf",
                          "file_format",
                          is_flag=True,
                          flag_value="pdf",
                          help="Generates a pdf document, useful for printing")

fill_color_option = click.option("--fill-color",
                                 type=str,
                                 default="white",
                                 show_default=True,
                                 help="Color to fill the shapes"
                                 )

stroke_color_option = click.option("--stroke-color",
                                   type=str,
                                   default="black",
                                   show_default=True,
                                   help="Color of the shapes' outlin4")

background_color_option = click.option("--background-color",
                                       type=str,
                                       default="white",
                                       show_default=True,
                                       help="Background color of the page")

stroke_width_option = click.option("--stroke-width",
                                   type=int,
                                   default=2,
                                   metavar="<int>",
                                   show_default=True,
                                   help="Width of the shapes' outline")

epilog = f"""\
Generates a template given the options.

'page' can be any of:

{', '.join(PAPERSIZE_MAP.keys())}

'stroke-color', 'fill-color' and 'background-color' can be hexadecimal "#xxxxxx"
values or ImageMagick Color Names
"""

@click.command(help="cmd help",
               epilog=epilog,
               short_help="sht hlp",
               options_metavar="[options]",
               no_args_is_help=False)
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
