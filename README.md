## drawing-templates-generator

### WAT

generates like this

```
./drawing-templates-generator.py --square --columns 6
```

![](https://github.com/iacchus/drawing-templates-generator/blob/main/square-000.png?raw=true)

and this

```
./drawing-templates-generator.py --circle --columns 8
```

![](https://github.com/iacchus/drawing-templates-generator/blob/main/circle-000.png?raw=true)

### dependencies

* python3 with pip
* python wand (and its dependencies)
* python click

```
pip install wand click
```

### usage

```
$ ./drawing-templates-generator.py --help

Usage: drawing-templates-generator.py [options]

  Generate drawing templates in png (for digital art) and pdf (to be printed)

Options:
  --width <width>             Width for the generated png image  [default:
                              1200]
  --height <height>           Height for the generated png image  [default:
                              2000]
  --spacing <spacing>         Margin/padding between the shapes, in pixels
                              [default: 33]
  --columns <num_of_cols>     How many shapes to draw in a line  [default: 6]
  --page <page_type>          Page format for pdf (see below)  [default: a4]
  --dpi <resolution>          Resolution for the pdf document  [default: 288]
  --square                    [shape] Use squares as shape  [default: square]
  --circle                    [shape] Use circles as shape
  --png                       [format] Generates a png image (for digital art)
                              [default: png]
  --pdf                       [format] Generates a pdf document, useful for
                              printing
  --stroke-width <width>      Width of the shapes' outline  [default: 2]
  --stroke-color <color>      Color of the shapes' outline (see below)
                              [default: black]
  --fill-color <color>        Color to fill the shapes (see below)  [default:
                              white]
  --background-color <color>  Background color of the page (see below)
                              [default: white]
  --help                      Show this message and exit.

  Generates a template given the options.

  'page' can be any of:

  4x6, 5x7, 7x9, 8x10, 9x11, 9x12, 10x13, 10x14, 11x17, 4A0, 2A0, a0, a1, a2,
  a3, a4, a4small, a5, a6, a7, a8, a9, a10, archa, archb, archC, archd, arche,
  b0, b1, b10, b2, b3, b4, b5, b6, b7, b8, b9, c0, c1, c2, c3, c4, c5, c6, c7,
  csheet, dsheet, esheet, executive, flsa, flse, folio, halfletter, isob0,
  isob1, isob10, isob2, isob3, isob4, isob5, isob6, isob7, isob8, isob9,
  jisb0, jisb1, jisb2, jisb3, jisb4, jisb5, jisb6, ledger, legal, letter,
  lettersmall, monarch, quarto, statement, tabloid

  'stroke-color', 'fill-color' and 'background-color' can be hexadecimal
  "#xxxxxx" values or ImageMagick Color Names; these are described at:

  https://imagemagick.org/script/color.php

  <https://github.com/iacchus/drawing-templates-generator>
```
