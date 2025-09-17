#!/usr/bin/env python

from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color

# Create a Drawing object
with Drawing() as draw:
    # Set the fill color for the square
    draw.fill_color = Color('blue')
    # Set the stroke color and width for the square's outline
    draw.stroke_color = Color('black')
    draw.stroke_width = 2

    # Define the rectangle coordinates (left, top, right, bottom)
    # For a square, ensure (right - left) equals (bottom - top)
    left = 50
    top = 50
    side_length = 100
    right = left + side_length
    bottom = top + side_length

    draw.rectangle(left=left, top=top, right=right, bottom=bottom)

    # Create an Image object to draw on
    with Image(width=200, height=200, background=Color('white')) as image:
        # Apply the drawing instructions to the image
        draw(image)
        # Save the image to a file
        image.save(filename='square.png')

print("Square drawn and saved as 'square.png'")
