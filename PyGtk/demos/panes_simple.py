#!/usr/bin/env python2
"""Paned Widgets simple

Paned Widgets divide their content area into two panes
with a divider in between that the user can adjust.
A separate child is placed into each pane.
"""

import pygtk
pygtk.require('2.0')
import gtk

class PanedWidgetsSimpleDemo(gtk.Window):
    def __init__(self, parent=None):
        # Create toplevel window
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_border_width(0)

	# rootbox
        rootbox = gtk.HBox(False, 0)
        self.add(rootbox)

        hpaned = gtk.HPaned()
	hpaned.set_border_width(5)

        rootbox.pack_start(hpaned, True, True)

        frame = gtk.Frame()
        frame.set_shadow_type(gtk.SHADOW_IN)
        frame.set_size_request(200, 80)
	button_l = gtk.Button("Left")
        frame.add(button_l)
	hpaned.add(frame)
	
        frame2 = gtk.Frame()
        frame2.set_shadow_type(gtk.SHADOW_IN)
        frame2.set_size_request(200, 80)
        
        button_r = gtk.Button("Right")
        frame2.add(button_r)
        hpaned.add2(frame2)

        self.show_all()



def main():
    PanedWidgetsSimpleDemo()
    gtk.main()

if __name__ == '__main__':
    main()
