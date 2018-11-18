#!/usr/bin/env python2
#region Description
'''Text Widget/TextViewBasic4

Insert Widget into Textview
Here: Image

Creates a TextView in a scrolled Window.

A widget can be added to a TextView using this method:

  `textview.add_child_in_window(child, which_window, xpos, ypos)`

where the child widget is placed in which_window at the location specified by `xpos` and `ypos`.

which_window indicates in which of the windows that make up the TextView the widget is to be placed:

  `gtk.TEXT_WINDOW_TEXT`

  `gtk.TEXT_WINDOW_TOP`
  `gtk.TEXT_WINDOW_BOTTOM`
  `gtk.TEXT_WINDOW_LEFT`
  `gtk.TEXT_WINDOW_RIGHT`
  `gtk.TEXT_WINDOW_WIDGET`
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

text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et" \
       " dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum." \
       " Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."
#endregion

class TextViewBasic4Demo(gtk.Window):

    def __init__(self, parent=None):

        #region Window init
        gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(400, 210)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=200, min_height=100)
        #endregion

        box1 = gtk.VBox(False, 0)

        self.add(box1)
        #region TextView

        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text(text)

        textview.set_wrap_mode(gtk.WRAP_WORD)
        sw1 = gtk.ScrolledWindow()
        sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw1.add(textview)

        image = gtk.Image()
        image.set_from_file(ICON_IMAGE)
        textview.add_child_in_window(image, gtk.TEXT_WINDOW_TEXT, 0, 0)
        box1.pack_start(sw1, True, True, 0)
        #endregion

        self.show_all()

def main():
    TextViewBasic4Demo()
    gtk.main()

if __name__ == '__main__':
    main()
