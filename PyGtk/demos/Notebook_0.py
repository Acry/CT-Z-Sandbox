#!/usr/bin/env python2
'''NoteBook/NoteBook0

The NoteBook Widget is a collection of "pages" that overlap each other;
each page contains different information with only one page visible at a time.
It is a good way to show blocks of similar information that warrant separation in their display.

The first function call you will need to know, is used to create a new notebook widget.

  notebook = gtk.Notebook()

Once the notebook has been created, there are a number of methods that operate on the notebook widget.

The first one we will look at is how to position the page indicators.
These page indicators or "tabs" as they are referred to, can be positioned in four ways:

top, bottom, left, or right

  notebook.set_tab_pos(pos)

pos will be one of the following, which are pretty self explanatory:

  pos = gtk.POS_LEFT
  pos = gtk.POS_RIGHT
  pos = gtk.POS_TOP
  pos = gtk.POS_BOTTOM

POS_TOP is the default.

There are three ways to add pages to a NoteBook.
Let's look at the first two together as they are quite similar.

  notebook.append_page(child, tab_label)
  notebook.prepend_page(child, tab_label)

  notebook.insert_page(child, tab_label, position)

the first page having position zero.

'''

import os
import gtk
import pygtk
pygtk.require('2.0')

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

text1 = "On my first day learning PyGTK I browsed the examples. " \
       "I had a lot of great ideas, but I was pretty sceptical since PyGtk is deprecated. " \
       "On the other hand... well it runs and I saw you can do a lot of things with it. "\
       "The API is stable, there is a lot of Demo-Code, Python 2 is not that different from "\
       "Python 3 and all those Hype-Jumpers are gone."

text2 = "First thing to do is...\n" \
        "Last thing to know is... "


class NoteBook0Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_border_width(10)
        self.set_default_size(500, 700)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)

        # New Notebook
        notebook = gtk.Notebook()
        # Set Position of Tabs
        pos = gtk.POS_LEFT
        notebook.set_tab_pos(pos)
        self.add(notebook)

        # Page 1
        textview1 = gtk.TextView()
        textbuffer = textview1.get_buffer()
        textbuffer.set_text(text1)
        textview1.set_wrap_mode(gtk.WRAP_WORD)
        sw1 = gtk.ScrolledWindow()
        sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw1.add(textview1)
        l1 = gtk.Label('')
        l1.set_text_with_mnemonic("Day 1")
        notebook.append_page(sw1, l1)

        # Page 2
        textview2 = gtk.TextView()
        textbuffer2 = textview2.get_buffer()
        textbuffer2.set_text(text2)
        textview2.set_wrap_mode(gtk.WRAP_WORD)
        sw2 = gtk.ScrolledWindow()
        sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw2.add(textview2)
        l2 = gtk.Label('')
        l2.set_text_with_mnemonic("Day 2")
        notebook.append_page(sw2, l2)
        self.show_all()


def main():
    gtk.main()


def main():
    NoteBook0Demo()
    gtk.main()

if __name__ == '__main__':
    main()
