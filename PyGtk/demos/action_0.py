#!/usr/bin/env python2
"""Action and ActionGroup/Action 0

An Action object represents an action that the user can take using an application user interface.
It contains information used by proxy UI elements (for example, MenuItems or Toolbar items) to present the action to the user.

For example, the standard File->Quit menu item can be represented with an icon, mnemonic text and accelerator.
When activated, the menu item triggers a callback that could exit the application.
Likewise a Toolbar Quit button could share the icon, mnemonic text and callback.
Both of these UI elements could be proxies of the same Action.

Ordinary Button, ToggleButton and RadioButton widgets can also act as proxies for an Action though there is no support for these in the UIManager.

An Action can be created using the constructor:
`action = gtk.Action(name, label, tooltip, stock_id)`

name is a string used to identify the Action in an ActionGroup or in a UIManager specification.
label and tooltip are strings used as the label and tooltip in proxy widgets.
If label is None then the stock_id must be a string specifying a Stock Item to get the label from.
If tooltip is None the Action will not have a tooltip.

Using Actions:
The basic procedure for using an Action with a Button proxy is illustrated by this demo.
The Button is connected to the Action using the method:
`action.connect_proxy(proxy)`

where proxy is a MenuItem, ToolItem or Button widget.

An Action has one signal the "activate" signal that is triggered when the Action is activated usually as the result of a proxy widget being activated (for example a ToolButton is clicked).
You just have connect a callback to this signal to handle the activation of any of the proxy widgets.
"""

import pygtk
pygtk.require('2.0')
import gtk
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
ICON_IMAGE = os.path.join(IMAGEDIR, 'gtk-logo.svg')


class Action0Demo(gtk.Window):
    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_default_size(70, 30)
        self.set_icon_from_file(ICON_IMAGE)
        self.set_geometry_hints(min_width=70, min_height=30)

        # Create an accelerator group
        accelgroup = gtk.AccelGroup()
        # Add the accelerator group to the toplevel window
        self.add_accel_group(accelgroup)

        # Create an action for quitting the program using a stock item
        action = gtk.Action('Quit', None, None, gtk.STOCK_QUIT)
        # Connect a callback to the action
        action.connect('activate', self.quit_cb)

        # Create an ActionGroup named SimpleAction
        actiongroup = gtk.ActionGroup('SimpleAction')
        # Add the action to the actiongroup with an accelerator
        # None means use the stock item accelerator
        actiongroup.add_action_with_accel(action, None)

        # Have the action use accelgroup
        action.set_accel_group(accelgroup)

        # Connect the accelerator to the action
        action.connect_accelerator()

        # Create the button to use as the action proxy widget
        quitbutton = gtk.Button()
        # add it to the window
        self.add(quitbutton)

        # Connect the action to its proxy widget
        action.connect_proxy(quitbutton)
        self.show_all()
        return

    def quit_cb(self, b):
        print 'Quitting program'
        if __name__ == '__main__':
            gtk.main_quit()
        else:
            self.destroy()


if __name__ == '__main__':
    Action0Demo()
    gtk.main()
