# -*- coding: utf-8 -*-
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')

from gi.repository import Pango, PangoCairo

import cairo
import sys

TEMPLATE_FILENAME = 'data/EtikettefuerKolla.png'
FONT_NAME = 'American Typewriter'
FONT_SIZE = 25
FONT_DESCRIPTION = Pango.FontDescription('{} {}'.format(FONT_NAME, FONT_SIZE))
TEXT_PORTION = 0.75

TOP_LEFT_CORNER = (25, 25)

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

    opts = cairo.FontOptions()
    opts.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    PangoCairo.context_set_font_options(layout.get_context(), opts)

    context.set_source_rgb(0, 0, 0)

    PangoCairo.update_layout(context, layout)
    PangoCairo.show_layout(context, layout)

    surf.write_to_png(output_file)
