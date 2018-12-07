#!/usr/bin/env python2
"""Windows/Scrolling 2

INFO HERE
"""

import pygtk
pygtk.require('2.0')
import gtk

class Scrolling2Demo(gtk.Window):
    def __init__(self, parent=None):
        # Create toplevel window
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_border_width(0)
        self.set_size_request(300, 300)
        # create a new scrolled window.
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_border_width(10)

        # the policy is one of POLICY AUTOMATIC, or POLICY_ALWAYS.
        # POLICY_AUTOMATIC will automatically decide whether you need
        # scrollbars, whereas POLICY_ALWAYS will always leave the scrollbars
        # there. The first one is the horizontal scrollbar, the second, the
        # vertical.
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_ALWAYS)

        
	# rootbox
        rootbox = gtk.VBox(False, 0)
        self.add(rootbox)
	rootbox.pack_start(scrolled_window, True, True, 0)

        # create a table of 10 by 10 squares.
        table = gtk.Table(10, 10, False)

        # set the spacing to 10 on x and 10 on y
        table.set_row_spacings(10)
        table.set_col_spacings(10)

        # pack the table into the scrolled window
        scrolled_window.add_with_viewport(table)

        # this simply creates a grid of toggle buttons on the table
        # to demonstrate the scrolled window.
        for i in range(10):
            for j in range(10):
                buffer = "button (%d,%d)" % (i, j)
                button = gtk.ToggleButton(buffer)
                table.attach(button, i, i+1, j, j+1)
                button.show()

        # Add a "close" button to the bottom of the dialog
        button = gtk.Button("close")


        # this makes it so the button is the default.
        button.set_flags(gtk.CAN_DEFAULT)
        rootbox.pack_start( button, True, True, 0)
        button.connect('clicked', lambda button, w=self: w.destroy())
        
        # This grabs this button to be the default button. Simply hitting
        # the "Enter" key will cause this button to activate.
        button.grab_default()
	self.show_all()

def main():
    Scrolling2Demo()
    gtk.main()

if __name__ == '__main__':
    main()
