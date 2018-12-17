#!/usr/bin/env python2
'''UI Manager/UI 0

A UIManager can be used to create the menus and toolbars for an application user interface as follows:

* Create a UIManager instance
* Extract the AccelGroup from the UIManager and add it to the top level Window
* Create the ActionGroup instances and populate them with the appropriate Action instances.
* Add the ActionGroup instances to the UIManager in the order that the Action instances should be found.
* Add the UI XML descriptions to the UIManager. Make sure that all Actions referenced by the descriptions are available in the UIManager ActionGroup instances.
* Extract references to the menubar, menu and toolbar widgets by name for use in building the user interface.
* Dynamically modify the user interface by adding and removing UI descriptions and by adding, rearranging and removing the associated ActionGroup instances.

A UIManager instance is created by the constructor:
  `uimamager = gtk.UIManager()`

A new UIManager is created with an associated AccelGroup that can be retrieved using the method:
  `accelgroup = uimanager.get_accel_group()`

The AccelGroup should be added to the top level window of the application so that the Action accelerators can be used by your users.
For example:
  `window = gtk.Window()`
  ...
  `uimanager = gtk.UIManager()`
  `accelgroup = uimanager.get_accel_group()`
  `window.add_accel_group(accelgroup)`
'''


import pygtk
pygtk.require('2.0')
import gobject
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

def activate_action(action):
    print 'Action "%s" activated' % action.get_name()

def activate_radio_action(action, current):
    print 'Radio action "%s" selected'% current.get_name()

class UI0Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_border_width(0)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=100, min_height=100)

        uimanager = gtk.UIManager()
        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)



        box1 = gtk.VBox(False, 0)
        self.add(box1)

        # box1.pack_start(ui.get_widget("/MenuBar"), False, False, 0)

        label = gtk.Label("Type\n<alt>\nto start")
        label.set_size_request(200, 200)
        label.set_alignment(0.5, 0.5)
        box1.pack_start(label, True, True, 0)

        separator = gtk.HSeparator()
        box1.pack_start(separator, False, True, 0)

        box2 = gtk.VBox(False, 10)
        box2.set_border_width(10)
        box1.pack_start(box2, False, True, 0)

        button = gtk.Button("close")
        button.connect("clicked", lambda b, w=self: w.destroy())
        box2.pack_start(button, True, True, 0)
        button.set_flags(gtk.CAN_DEFAULT)
        button.grab_default()

        self.show_all()


if __name__ == '__main__':
    UI0Demo()
    gtk.main()
