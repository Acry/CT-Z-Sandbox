#!/usr/bin/env python2
'''Drag and Drop/_0

PyGTK has a high level set of functions for doing inter-process communication via the drag-and-drop system.
PyGTK can perform drag-and-drop on top of the low level Xdnd and Motif drag-and-drop protocols.

An application capable of drag-and-drop first defines and sets up the widget(s) for drag-and-drop.
Each widget can be a source and/or destination for drag-and-drop.
Note that these widgets must have an associated X Window.

Source widgets can send out drag data, thus allowing the user to drag things off of them, while destination widgets
can receive drag data. Drag-and-drop destinations can limit who they accept drag data from, e.g. the same application
or any application (including itself).

Sending and receiving drop data makes use of signals. Dropping an item to a destination widget requires both a data
request (for the source widget) and data received signal handler (for the target widget).

Additional signal handlers can be connected if you want to know when a drag begins (at the very instant it starts),
to when a drop is made, and when the entire drag-and-drop procedure has ended (successfully or not).

Your application will need to provide data for source widgets when requested, that involves having a drag data request
signal handler. For destination widgets they will need a drop data received signal handler.

__So a typical drag-and-drop cycle would look as follows:__

* Drag begins. Source can get "drag-begin" signal. Can set up drag icon, etc.

* Drag moves over a drop area. Destination can get "drag-motion" signal.

* Drop occurs. Destination can get "drag-drop" signal. Destination should ask for source data.

* Drag data request (when a drop occurs). Source can get "drag-data-get" signal.

* Drop data received (may be on same or different application). Destination can get "drag-data-received" signal.

* Drag data delete (if the drag was a move). Source can get "drag-data-delete" signal

* Drag-and-drop procedure done. Source can receive "drag-end" signal.

There are a few minor steps that go in between here and there.

__DND Properties

This program prints out the targets of a drag operation.
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'apple-red.png')

class _0Demo(gtk.Window):
    def motion_cb(self, wid, context, x, y, time):
        context.drag_status(gtk.gdk.ACTION_COPY, time)
        return True

    def drop_cb(self, wid, context, x, y, time, label):
        label.set_text('\n'.join([str(t) for t in context.targets]))
        context.finish(True, False, time)
        return True

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
        label = gtk.Label()
        self.add(label)
        self.drag_dest_set(0, [], 0)
        self.connect('drag_motion', self.motion_cb)
        self.connect('drag_drop', self.drop_cb, label)

        self.show_all()


def main():
    _0Demo()
    gtk.main()

if __name__ == '__main__':
    main()
