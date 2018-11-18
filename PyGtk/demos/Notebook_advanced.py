#!/usr/bin/env python2
'''NoteBook/NoteBookAdvanced

This time we have a pixbuff as background.

'''

import pygtk
pygtk.require('2.0')
import gtk
import os
import pango

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')
IMAGE = "squares2.png"
MAIN_IMAGE = os.path.join(IMAGEDIR, IMAGE)

text1 = "On my first day learning PyGTK I browsed the examples. " \
       "I had a lot of great ideas, but I was pretty sceptical since PyGtk is deprecated. " \
       "On the other hand... well it runs and I saw you can do a lot of things with it. "\
       "The API is stable, there is a lot of Demo-Code, Python 2 is not that different from "\
       "Python 3 and all those Hype-Jumpers are gone."

text2 = "First thing to do is...\n" \
        "Last thing to know is... "


class NoteBookAdvancedDemo(gtk.Window):
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

        pixbuf = gtk.gdk.pixbuf_new_from_file(MAIN_IMAGE)
        pixmap, mask = pixbuf.render_pixmap_and_mask()

        # New Notebook
        notebook = gtk.Notebook()
        pos = gtk.POS_LEFT
        notebook.set_tab_pos(pos)
        self.add(notebook)

        font = pango.FontDescription('Indie Flower 20')

        # Page 1
        textview1 = gtk.TextView()
        textbuffer = textview1.get_buffer()
        layout = textview1.create_pango_layout(text1)
        layout.set_spacing(pango.SCALE * 1000)
        textbuffer.set_text(text1)
        textview1.modify_font(font)
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
        textview2.modify_font(font)
        textview2.set_wrap_mode(gtk.WRAP_WORD)
        sw2 = gtk.ScrolledWindow()
        sw2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        sw2.add(textview2)
        l2 = gtk.Label('')
        l2.set_text_with_mnemonic("Day 2")
        notebook.append_page(sw2, l2)

        notebook.set_current_page(2)
        self.show_all()
        # Set Backgrounds
        textview1.realize()
        tvwindow = textview1.get_window(gtk.TEXT_WINDOW_TEXT)
        tvwindow.set_back_pixmap(pixmap, gtk.FALSE)
        textview2.realize()
        tvwindow = textview2.get_window(gtk.TEXT_WINDOW_TEXT)
        tvwindow.set_back_pixmap(pixmap, gtk.FALSE)
        del pixbuf, pixmap

def main(self):
    gtk.main()

def main():
    NoteBookAdvancedDemo()
    gtk.main()

if __name__ == '__main__':
    main()
