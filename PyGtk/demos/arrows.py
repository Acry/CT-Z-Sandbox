#!/usr/bin/env python2
"""Arrow Widget

The Arrow widget produces an arrow pointing in one of the four cardinal directions and has 4 possible styles.
It can be useful when placed on a button. Like the Label widget, it emits no signals.

There are only two calls for manipulating an Arrow widget:
`arrow = gtk.Arrow(arrow_type, shadow_type)`

`arrow.set(arrow_type, shadow_type)`

The first creates a new arrow widget with the indicated type and appearance. The second allows these values to be altered retrospectively.

The arrow_type argument may take one of the following values:
  ARROW_UP
  ARROW_DOWN
  ARROW_LEFT
  ARROW_RIGHT

These values obviously indicate the direction in which the arrow will point. The shadow_type argument may take one of these values:
  SHADOW_IN
  SHADOW_OUT            # the default
  SHADOW_ETCHED_IN
  SHADOW_ETCHED_OUT

A `gtk.Arrow` will fill any space allotted to it, but since it is inherited from `gtk.Misc`, it can be padded and/or aligned, to fill exactly the space desired.
"""

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')


def create_arrow_button(arrow_type, shadow_type):
    """Create an Arrow widget with the specified parameters and pack it into a button"""
    button = gtk.Button()
    arrow = gtk.Arrow(arrow_type, shadow_type)
    button.add(arrow)
    button.show()
    arrow.show()
    return button


class ArrowWidgetDemo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_icon_from_file(ICON_IMAGE)

        # Create a box to hold the arrows/buttons
        box = gtk.HBox(False, False)
        box.set_border_width(2)
        self.add(box)

        # Pack and show all our widgets
        box.show()

        button = create_arrow_button(gtk.ARROW_UP, gtk.SHADOW_IN)
        box.pack_start(button, False, False, 3)

        button = create_arrow_button(gtk.ARROW_DOWN, gtk.SHADOW_OUT)
        box.pack_start(button, False, False, 3)
  
        button = create_arrow_button(gtk.ARROW_LEFT, gtk.SHADOW_ETCHED_IN)
        box.pack_start(button, False, False, 3)
  
        button = create_arrow_button(gtk.ARROW_RIGHT, gtk.SHADOW_ETCHED_OUT)
        box.pack_start(button, False, False, 3)

        self.show_all()


if __name__ == '__main__':
    ArrowWidgetDemo()
    gtk.main()
