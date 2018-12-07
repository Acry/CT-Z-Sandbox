#!/usr/bin/env python2
#region Description
'''Text Widget/TextViewBasic6a

You can tag text as invisible in the text buffer.
`visibility_tag = textbuffer.create_tag(None, invisible=True)`
The so tagged text isn't rendered.

Implement:
* Text Folding
* get selection
`start, end = textbuffer.get_selection_bounds()`
* hide selection
`invisibility_tag = textbuffer.create_tag(None, invisible=True)`
* insert button at selection start

 to hide/unhide
`invisibility_tag = textbuffer.create_tag(None, invisible=True)`
`visibility_tag = textbuffer.create_tag(None, invisible=False)`
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

text = "Read and show png from from Cherrytree sqlite db (ctb).\n" \
       "call with ctb.\n" \
       "`$ python2 ctb_image_reader.py example.ctb`\n"   \
       "navigate with arrow keys:\n" \
       "left/right step back and forth\n"   \
       "up first entry / down last entry\n "
#endregion
def create_toggler(widget, data=None):
    button = gtk.ToggleButton("toggle button 1")
    # When the button is toggled, we call the "callback" method
    # with a pointer to "button" as its argument
    button.connect("toggled", callback, "toggle button 1")
    (button, True, True, 2)
    # iter = textbuffer.get_iter_at_line(2)
    # anchor = textbuffer.create_child_anchor(iter)
    # textview.add_child_at_anchor(button, anchor)


def callback(widget, data=None):
    print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])

def cb(widget, textview, data=None):
    gtk.MenuItem(label="foo", use_underline=True)
    print "yep"

def cb2(textview, menu, anchor):
        """Extend the Default Right-Click Menu of the CodeBox"""
        # textview.menu_populate_popup(menu, menus.get_popup_menu_entries_codebox(self), self.dad.orphan_accel_group)
        pass

class TextViewBasic6aDemo(gtk.Window):
    def __init__(self, parent=None):
        #region Window init
        gtk.Window.__init__(self)

        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(600, 600)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=200, min_height=100)
        #endregion

        #region TextView
        textview = gtk.TextView()
        textbuffer = textview.get_buffer()
        textbuffer.set_text(text)
        textview.set_wrap_mode(gtk.WRAP_WORD)

        sw1 = gtk.ScrolledWindow()
        sw1.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

        self.add(sw1)
        sw1.add(textview)
        #endregion
        # textview.connect("", create_toggler,)
        # invisibility_tag = textbuffer.create_tag(None, invisible=True)
        visibility_tag = textbuffer.create_tag(None, invisible=True)
        # Gtk.TextView.signals.populate_popup(text_view, popup)
        textview.connect("populate_popup", cb, textview)
        # menu = textview.
        print dir(textview)
        #Connect to the populate-popup signal, and add your menu item to the Gtk.Menu
        # that is passed to your signal handler.

        #region Search Backtick and set invisible, markup
        tag = textbuffer.create_tag(None, background="lightgrey", background_full_height=True, style=pango.STYLE_OBLIQUE, font="Inconsolta")
        tag_string = "`"
        start, end = textbuffer.get_bounds()
        tag_start = None
        tag_end = None
        searching = True
        count = 0
        while searching:
            try:
                match_start, match_end = start.forward_search(tag_string, gtk.TEXT_SEARCH_TEXT_ONLY, limit=None)
                if not count % 2:
                    # first
                    tag_start = match_start.copy()
                    tag_start.forward_char()
                else:
                    # second
                    tag_end = match_end.copy()
                    tag_end.backward_char()
                    textbuffer.apply_tag(tag, tag_start, tag_end)
                textbuffer.apply_tag(visibility_tag, match_start, match_end)
                start = match_end
                count = count + 1
            except:
                searching = False
        print "Found the Tag-Marker: " + tag_string, count, "times"
        #endregion
        self.show_all()


def main():
    TextViewBasic6aDemo()
    gtk.main()


if __name__ == '__main__':
    main()
