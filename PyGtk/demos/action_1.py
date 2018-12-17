#!/usr/bin/env python2
"""Action and ActionGroup/Action 1

Creating Proxy Widgets
"""

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')


class Action1Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(350, 250)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=350, min_height=250)

        vbox = gtk.VBox()
        vbox.show()
        self.add(vbox)

        accelgroup = gtk.AccelGroup()
        self.add_accel_group(accelgroup)

        # Create an action for quitting the program using a stock item
        action = gtk.Action('Quit', '_Quit me!', 'Quit the Program',
                            gtk.STOCK_QUIT)
        action.set_property('short-label', '_Quit')
        # Connect a callback to the action
        action.connect('activate', self.quit_cb)

        # Create an ActionGroup named BasicAction
        actiongroup = gtk.ActionGroup('BasicAction')
        # Add the action to the actiongroup with an accelerator
        # None means use the stock item accelerator
        actiongroup.add_action_with_accel(action, None)

        # Have the action use accelgroup
        action.set_accel_group(accelgroup)

        # Create a MenuBar
        menubar = gtk.MenuBar()
        menubar.show()
        vbox.pack_start(menubar, False)

        # Create the File Action and MenuItem
        file_action = gtk.Action('File', '_File', None, None)
        actiongroup.add_action(file_action)
        file_menuitem = file_action.create_menu_item()
        menubar.append(file_menuitem)

        # Create the File Menu
        file_menu = gtk.Menu()
        file_menuitem.set_submenu(file_menu)

        # Create a proxy MenuItem
        menuitem = action.create_menu_item()
        file_menu.append(menuitem)

        # Create a Toolbar
        toolbar = gtk.Toolbar()
        toolbar.show()
        vbox.pack_start(toolbar, False)

        # Create a proxy ToolItem
        toolitem = action.create_tool_item()
        toolbar.insert(toolitem, 0)

        # Create and pack a Label
        label = gtk.Label('''
        Select File->Quit me! or
        click the toolbar Quit button or
        click the Quit button below or
        press Control+q
        to quit.
        ''')
        label.show()
        vbox.pack_start(label)

        # Create a button to use as another proxy widget
        quitbutton = gtk.Button()
        # add it to the window
        vbox.pack_start(quitbutton, False)

        # Connect the action to its proxy widget
        action.connect_proxy(quitbutton)
        # Have to set tooltip after toolitem is added to toolbar
        action.set_property('tooltip', action.get_property('tooltip'))
        tooltips = gtk.Tooltips()
        tooltips.set_tip(quitbutton, action.get_property('tooltip'))
        self.show()

    def quit_cb(self, b):
        print 'Quitting program'
        if __name__ == '__main__':
            gtk.main_quit()
        else:
            self.destroy()


if __name__ == '__main__':
    Action1Demo()
    gtk.main()
