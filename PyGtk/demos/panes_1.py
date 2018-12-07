#!/usr/bin/env python2
"""Paned Widgets/HPaned 2

Trying to remove, not hide, a widget during runtime.
Press 'close me' button, it should vanish and reappear after a second.
"""
import pygtk
pygtk.require('2.0')
import gtk
import gobject


class HPaned2Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_border_width(0)

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

        self.button_r = gtk.Button("Close me")
        self.button_r.connect("clicked", self.switch, hpaned, frame2)
        frame2.add(self.button_r)
        hpaned.add2(frame2)

        self.show_all()

    def switch(self, data, hpaned, frame):
        timer = gobject.timeout_add(1000, self.add_frame, hpaned, frame)
        hpaned.remove(frame)

    def add_frame(self, hpaned, frame):
        hpaned.add2(frame)


if __name__ == '__main__':
    HPaned2Demo()
    gtk.main()
