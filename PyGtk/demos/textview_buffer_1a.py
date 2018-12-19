#!/usr/bin/env python2
"""Text Widget/Buffer 1a

Check modification:

You get a green light if the buffer is not modified, a red light if it is, afer 2 seconds it gonna turn green again.
"""

import pygtk
pygtk.require('2.0')
import gtk
import os
import gobject

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
BUTTON_RED = os.path.join(IMAGEDIR, 'Button-Red.svg')
BUTTON_GREEN = os.path.join(IMAGEDIR, 'Button-Green.svg')
CHECK_TIME = 1000 * 2  # 1000 ms * 2 = 2 seconds

text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."


class Buffer1aDemo(gtk.Window):
    def green_light(self):
        gobject.source_remove(self.timer)
        self.imagebox.remove(self.light_red)
        self.imagebox.pack_end(self.light_green, False, False)
        self.light_green.show()

    def is_modifed(self, data):
        if self.imagebox.get_children()[0] is self.light_green:
            self.imagebox.remove(self.light_green)
            self.imagebox.pack_end(self.light_red, False, False)
            self.light_red.show()
            self.timer = gobject.timeout_add(CHECK_TIME, self.green_light)
        else:
            gobject.source_remove(self.timer)
            self.timer = gobject.timeout_add(CHECK_TIME, self.green_light)

    def __init__(self, parent=None):
        self.timer = None
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(500, 250)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)

        # box that catches everything else
        rootbox = gtk.VBox(homogeneous=False)
        self.add(rootbox)

        # top
        self.imagebox = gtk.HBox(homogeneous=False)
        rootbox.pack_start(self.imagebox, False, False)

        # lights
        self.light_green = gtk.Image()
        self.light_green.set_from_file(BUTTON_GREEN)
        self.light_green.set_tooltip_text("Not modified")

        self.light_red = gtk.Image()
        self.light_red.set_from_file(BUTTON_RED)
        self.light_red.set_tooltip_text("Modified")

        # start with a green light
        self.imagebox.pack_end(self.light_green, False, False)

        # TextView in scrolled window
        textview = gtk.TextView()
        self.textbuffer = textview.get_buffer()
        self.textbuffer.set_text(text)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw.add(textview)
        rootbox.pack_start(sw, expand=True, fill=True)
        self.textbuffer.connect("changed", self.is_modifed)
        self.show_all()


if __name__ == '__main__':
    Buffer1aDemo()
    gtk.main()

