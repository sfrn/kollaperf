# -*- coding: utf-8 -*-
import sys
import logging
import subprocess
from tempfile import NamedTemporaryFile

import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')

from gi.repository import Pango, PangoCairo

TEMPLATE_FILENAME = 'data/EtikettefuerKolla.png'
FONT_NAME = 'American Typewriter'
FONT_SIZE = 35
FONT_DESCRIPTION = Pango.FontDescription('{} {}'.format(FONT_NAME, FONT_SIZE))
TEXT_PORTION = 0.75

TOP_LEFT_CORNER = (25, 25)
PRINTER_NAME = 'QL-550'

logger = logging.getLogger(__name__)

def generate_label(text, output_file, font_description=FONT_DESCRIPTION):
    surf = cairo.ImageSurface.create_from_png(TEMPLATE_FILENAME)
    context = cairo.Context(surf)
    context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

    context.translate(TOP_LEFT_CORNER[0], TOP_LEFT_CORNER[1])

    layout = PangoCairo.create_layout(context)
    layout.set_font_description(font_description)
    layout.set_text(text, len(text))
    layout.set_width((TEXT_PORTION * surf.get_width() - TOP_LEFT_CORNER[0])
                    * Pango.SCALE)
    layout.set_height((surf.get_height() - TOP_LEFT_CORNER[1]) * Pango.SCALE)
    layout.set_ellipsize(Pango.EllipsizeMode.END)

    opts = cairo.FontOptions()
    opts.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    PangoCairo.context_set_font_options(layout.get_context(), opts)

    context.set_source_rgb(0, 0, 0)

    PangoCairo.update_layout(context, layout)
    PangoCairo.show_layout(context, layout)

    surf.write_to_png(output_file)

def print_filename(filename, printer=PRINTER_NAME):
    proc = subprocess.Popen(['lp', '-d', printer, filename])
    if proc.wait() != 0:
        raise RuntimeError("Couldn't print!")

def generate_and_print(text):
    with NamedTemporaryFile() as f:
        logger.info('Generate {!r} to {!r} ...'.format(text, f.name))
        generate_label(text, f.name)
        f.flush()
        print_filename(f.name)
