#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''Text Widget/Iters

Text Buffers
A TextBuffer is the core component of the PyGTK text editing system.
It contains the text, the TextTags in a TextTagTable and the TextMarks which together describe how the text is to be
displayed and allow a user to interactively modify the text and text display.
A TextBuffer is associated with one or more TextViews which display the TextBuffer contents.

A TextBuffer can be created automatically when a TextView is created or it can be created with the function:
`textbuffer = TextBuffer(table=None)`
where table is a TextTagTable, if table is not specified (or is `None`) a TextTagTable will be created for the
TextBuffer.

In this example I show the buffer status information and set the cursor to a certain position using an iter.

You can retrieve the number of lines in a textbuffer by using the method:
`line_count = textbuffer.get_line_count()`

Likewise you can get the number of characters in the textbuffer using:
`char_count = textbuffer.get_char_count()`

When the textbuffer contents are changed the modified flag in the textbuffer is set.

iter (plural iters) from Latin iter (“passage”).
Here: a text passage.

An Iter is used to specify a volatile location within a Buffer between two characters.
TextBuffer methods that manipulate text use TextIters to specify where the method is to be applied.

`iter = textbuffer.get_iter_at_offset(char_offset)`

`iter = textbuffer.get_iter_at_line(line_number)`

`iter = textbuffer.get_iter_at_line_offset(line_number, line_offset)`

`iter = textbuffer.get_iter_at_mark(mark)`


`startiter = textbuffer.get_start_iter()`

`enditer = textbuffer_get_end_iter()`

`startiter, enditer = textbuffer.get_bounds()`

`start, end = textbuffer.get_selection_bounds()`

Here I set the cursor to the beginning of line 2.
`iter = textbuffer.get_iter_at_line(2)`
`textbuffer.place_cursor(iter)`
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et"\
       "dolore magna aliquyam erat, sed diam voluptua.\n At vero eos et accusam et justo duo dolores et ea rebum.\n"\
       "Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet."


class TextViewItersDemo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(500, 250)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)
        rootbox = gtk.VBox()
        self.add(rootbox)
        #region TextView
        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text(text)
        textview.set_wrap_mode(gtk.WRAP_WORD)
        #endregion
        line_count = textbuffer.get_line_count()
        char_count = textbuffer.get_char_count()
        Label_text ="Lines: " + str(line_count) + ", Chars: " + str(char_count)
        rootbox.pack_start(textview)
        status_bar = gtk.InfoBar()
        rootbox.pack_start(status_bar, False, False)
        status_bar.set_message_type(gtk.MESSAGE_INFO)
        status_bar.get_content_area().pack_start(
                gtk.Label(Label_text),
                False, False)
        iter = textbuffer.get_iter_at_line(2)
        textbuffer.place_cursor(iter)
        self.show_all()

def main():
    TextViewItersDemo()
    gtk.main()

if __name__ == '__main__':
    main()
