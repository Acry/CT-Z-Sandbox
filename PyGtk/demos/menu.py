#!/usr/bin/env python2
'''Menu/MenuB1

There are three widgets that go into making a menubar and submenus:
* a menubar, which is a container for each of the individual menus.
* a menu, which acts as a container for the menu items, and
* a menu item, which is what the user wants to select, e.g., "Save"

This is slightly complex by the fact that menu item widgets are used for two different things.
They are both the widgets that are packed into the menu, and the widget that is packed into the menubar, which, when selected, activates the menu.

Look at the functions that are used to create menus and menubars.
The first function is used to create a new menubar:
`menu_bar = gtk.MenuBar()`

Use the `gtk.Container` `add()` method to pack this into a window, or the `gtk.Box` pack methods to pack it into a box - the same as buttons.

`menu = gtk.Menu()`
This function returns a reference to a new menu;
it is never actually shown (with the `show()` method), it is just a container for the menu items.

The next function is used to create menu items that are packed into the menu (and menubar):
`menu_item = gtk.MenuItem(label=None)`

The label, if any, will be parsed for mnemonic characters.
This call is used to create the menu items that are to be displayed.
Remember to differentiate between a "menu" as created with `gtk.Menu()` and a "menu item" as created by the `gtk.MenuItem()` functions.
The menu item will be an actual button with an associated action, whereas a menu will be a container holding menu items.
'''

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')

class MenuB1Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda w: gtk.main_quit())
        self.set_title(self.__class__.__name__)
        self.set_default_size(400, 450)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=200, min_height=100)

        # Init the menu-widget, and remember -- never
        # show() the menu widget!
        # This is the menu that holds the menu items, the one that
        # will pop up when you click on the "Root Menu" in the app
        menu = gtk.Menu()
        item_name = "Insert action"
        # Create a new menu-item with a name...
        menu_item = gtk.MenuItem(label=item_name)
        menu.append(menu_item)

        # Do something interesting when the menuitem is selected
        menu_item.connect("activate", self.menuitem_response, item_name)

        # This is the root menu, and will be the label
        # displayed on the menu bar.  There won't be a signal handler attached,
        # as it only pops up the rest of the menu when pressed.
        root_menu = gtk.MenuItem("Menu")
        # Now we specify that we want our newly created "menu" to be the
        # menu for the "root menu"
        root_menu.set_submenu(menu)

        # A vbox to put a menu and a button in:
        vbox = gtk.VBox(False, 0)
        self.add(vbox)

        # Create a menu-bar to hold the menus and add it to our main window
        menu_bar = gtk.MenuBar()
        vbox.pack_start(menu_bar, False, False, 2)

        # And finally we append the menu-item to the menu-bar -- this is the
        # "root" menu-item I have been raving about =)
        menu_bar.append(root_menu)

        self.show_all()

    # Print a string when a menu item is selected
    def menuitem_response(self, widget, string):
        print "%s" % string




if __name__ == '__main__':
    MenuB1Demo()
    gtk.main()
