#!/usr/bin/env python2
#region Description
'''Text Widget/Add Widget Image 2

Insert Image to Textview.
'''
#endregion

#region Import
import pygtk
pygtk.require('2.0')
import gtk
import os
import pango
#endregion

#region Constants
IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
FOURIER_IMAGE = os.path.join(IMAGEDIR, "Fourier_series_square_wave_circles_animation.gif")

text = "Press on this button:" \
       " dolore magna aliquyam erat, sed diam voluptua.\n At vero eos et accusam et justo duo dolores et ea rebum.\n" \
       " Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.\n"
#endregion


class AddWidgetImage2Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_default_size(400, 450)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=200, min_height=100)

        box1 = gtk.VBox(False, 0)
        self.add(box1)

        textview = gtk.TextView()
        textbuffer = textview.get_buffer()

        textbuffer.set_text(text)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        sw1 = gtk.ScrolledWindow()
        sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw1.add(textview)
        box1.pack_start(sw1, True, True, 0)
        iter = textbuffer.get_iter_at_line(2)
        pixbufanim = gtk.gdk.PixbufAnimation(FOURIER_IMAGE)
        image = gtk.Image()
        image.set_from_animation(pixbufanim)
        button = gtk.Button()
        button.add(image)

        anchor = textbuffer.create_child_anchor(iter)
        textview.add_child_at_anchor(button, anchor)

        self.show_all()


if __name__ == '__main__':
    AddWidgetImage2Demo()
    gtk.main()
