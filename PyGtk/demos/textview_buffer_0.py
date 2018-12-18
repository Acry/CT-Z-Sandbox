#!/usr/bin/env python2
"""Text Widget/Buffer 0

Buffer basics:

A TextBuffer is the core component of the PyGTK text editing system.
It stores attributed text for display in a view.
The TextBuffer is associated with one or more TextViews or SourceViews which display the TextBuffer contents.

A TextBuffer can be created automatically when a TextView is created
`textview = gtk.TextView()`

or it can be created with the function:
`textbuffer = TextBuffer(None)`

Text can be bound to the buffer with:
`textbuffer.set_text(text)`

Or retrieved the bound buffer:
`textview.get_buffer()`

Bind the buffer to a view.
`textview.set_buffer()`

This Demo builds one view and switches buffers on click.
"""

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

text1 = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."

text2 = "Click to switch the view's associated text-buffer."


class Buffer0Demo(gtk.Window):
    def clicked(self, widget, event):
        current_buffer = widget.get_buffer()
        if current_buffer is self.textbuffer1:
            widget.set_buffer(self.textbuffer2)
        else:
            widget.set_buffer(self.textbuffer1)

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(200, 200)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)

        #region TextView and Buffers

        #construct TextView

        # create view and use named, existing buffer
        # textview = gtk.TextView(buffer=self.textbuffer1)
        textview = gtk.TextView()
        textview.connect('button-press-event', self.clicked)

        self.textbuffer1 = gtk.TextBuffer(None)
        self.textbuffer2 = textview.get_buffer()

        #fill TextBuffers
        self.textbuffer1.set_text(text1)
        self.textbuffer2.set_text(text2)

        #set wrapping type
        textview.set_wrap_mode(gtk.WRAP_WORD)
        #add to container (in this case a window)
        self.add(textview)
        #endregion

        self.show_all()


if __name__ == '__main__':
    Buffer0Demo()
    gtk.main()

