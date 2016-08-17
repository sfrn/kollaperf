# -*- coding: utf-8 -*-
import sys
import logging
import subprocess
from tempfile import NamedTemporaryFile

from .config import settings

label_settings = settings['label']

import cairo
import gi
gi.require_version('Pango', '1.0')
gi.require_version('PangoCairo', '1.0')

from gi.repository import Pango, PangoCairo

logger = logging.getLogger(__name__)

FONT_DESCRIPTION = Pango.FontDescription('{} {}'.format(label_settings['font_name'],
                                                        label_settings['font_size']))

def generate_label(text, output_file):
    surf = cairo.ImageSurface.create_from_png(label_settings['template_filename'])
    context = cairo.Context(surf)
    context.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

    context.translate(*label_settings['top_left_corner'])

    layout = PangoCairo.create_layout(context)
    layout.set_font_description(FONT_DESCRIPTION)
    layout.set_text(text, len(text))
    layout.set_width((label_settings['text_portion'] * surf.get_width() - label_settings['top_left_corner'][0])
                    * Pango.SCALE)
    layout.set_height((surf.get_height() - label_settings['top_left_corner'][1]) * Pango.SCALE)
    layout.set_ellipsize(Pango.EllipsizeMode.END)

    opts = cairo.FontOptions()
    opts.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    PangoCairo.context_set_font_options(layout.get_context(), opts)

    context.set_source_rgb(0, 0, 0)

    PangoCairo.update_layout(context, layout)
    PangoCairo.show_layout(context, layout)

    surf.write_to_png(output_file)

def print_filename(filename, printer=label_settings['printer_name']):
    proc = subprocess.Popen(['lp', '-d', printer, filename], stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode != 0:
        raise RuntimeError("Couldn't print: {!r}".format(stderr))

def generate_and_print(text):
    with NamedTemporaryFile() as f:
        logger.info('Generate {!r} to {!r} ...'.format(text, f.name))
        generate_label(text, f.name)
        f.flush()
        print_filename(f.name)
