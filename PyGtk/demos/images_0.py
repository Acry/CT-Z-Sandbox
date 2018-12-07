#!/usr/bin/env python2
'''Images/Images2
Render some images from:
PixbufAnimation, Pixbuf, ImageFromFile, ImageFromStockItem, inline ImageFromXPM.

some relevant Methods:
`gtk.Image`
`image.set_from_file`

`gtk.gdk.PixbufAnimation`
`set_from_animation`

`gtk.gdk.pixmap_create_from_xpm_d()`

See:
https://developer.gnome.org/pygtk/stable/class-gdkpixmap.html
'''

import os

import pygtk
pygtk.require('2.0')
import gobject
import gtk

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
GOALIE_IMAGE = os.path.join(IMAGEDIR, "goalie.gif")

REDAPPLE_IMAGE = os.path.join(IMAGEDIR, "apple-red.png")
IMPORTANT_IMAGE = os.path.join(IMAGEDIR, "important.tif")
SOCCERBALL_IMAGE = os.path.join(IMAGEDIR, "soccerball.gif")

# XPM
WheelbarrowFull_xpm = [
"48 48 64 1",
"       c None",
".      c #DF7DCF3CC71B",
"X      c #965875D669A6",
"o      c #71C671C671C6",
"O      c #A699A289A699",
"+      c #965892489658",
"@      c #8E38410330C2",
"#      c #D75C7DF769A6",
"$      c #F7DECF3CC71B",
"%      c #96588A288E38",
"&      c #A69992489E79",
"*      c #8E3886178E38",
"=      c #104008200820",
"-      c #596510401040",
";      c #C71B30C230C2",
":      c #C71B9A699658",
">      c #618561856185",
",      c #20811C712081",
"<      c #104000000000",
"1      c #861720812081",
"2      c #DF7D4D344103",
"3      c #79E769A671C6",
"4      c #861782078617",
"5      c #41033CF34103",
"6      c #000000000000",
"7      c #49241C711040",
"8      c #492445144924",
"9      c #082008200820",
"0      c #69A618611861",
"q      c #B6DA71C65144",
"w      c #410330C238E3",
"e      c #CF3CBAEAB6DA",
"r      c #71C6451430C2",
"t      c #EFBEDB6CD75C",
"y      c #28A208200820",
"u      c #186110401040",
"i      c #596528A21861",
"p      c #71C661855965",
"a      c #A69996589658",
"s      c #30C228A230C2",
"d      c #BEFBA289AEBA",
"f      c #596545145144",
"g      c #30C230C230C2",
"h      c #8E3882078617",
"j      c #208118612081",
"k      c #38E30C300820",
"l      c #30C2208128A2",
"z      c #38E328A238E3",
"x      c #514438E34924",
"c      c #618555555965",
"v      c #30C2208130C2",
"b      c #38E328A230C2",
"n      c #28A228A228A2",
"m      c #41032CB228A2",
"M      c #104010401040",
"N      c #492438E34103",
"B      c #28A2208128A2",
"V      c #A699596538E3",
"C      c #30C21C711040",
"Z      c #30C218611040",
"A      c #965865955965",
"S      c #618534D32081",
"D      c #38E31C711040",
"F      c #082000000820",
"                                                ",
"          .XoO                                  ",
"         +@#$%o&                                ",
"         *=-;#::o+                              ",
"           >,<12#:34                            ",
"             45671#:X3                          ",
"               +89<02qwo                        ",
"e*                >,67;ro                       ",
"ty>                 459@>+&&                    ",
"$2u+                  ><ipas8*                  ",
"%$;=*                *3:.Xa.dfg>                ",
"Oh$;ya             *3d.a8j,Xe.d3g8+             ",
" Oh$;ka          *3d$a8lz,,xxc:.e3g54           ",
"  Oh$;kO       *pd$%svbzz,sxxxxfX..&wn>         ",
"   Oh$@mO    *3dthwlsslszjzxxxxxxx3:td8M4       ",
"    Oh$@g& *3d$XNlvvvlllm,mNwxxxxxxxfa.:,B*     ",
"     Oh$@,Od.czlllllzlmmqV@V#V@fxxxxxxxf:%j5&   ",
"      Oh$1hd5lllslllCCZrV#r#:#2AxxxxxxxxxcdwM*  ",
"       OXq6c.%8vvvllZZiqqApA:mq:Xxcpcxxxxxfdc9* ",
"        2r<6gde3bllZZrVi7S@SV77A::qApxxxxxxfdcM ",
"        :,q-6MN.dfmZZrrSS:#riirDSAX@Af5xxxxxfevo",
"         +A26jguXtAZZZC7iDiCCrVVii7Cmmmxxxxxx%3g",
"          *#16jszN..3DZZZZrCVSA2rZrV7Dmmwxxxx&en",
"           p2yFvzssXe:fCZZCiiD7iiZDiDSSZwwxx8e*>",
"           OA1<jzxwwc:$d%NDZZZZCCCZCCZZCmxxfd.B ",
"            3206Bwxxszx%et.eaAp77m77mmmf3&eeeg* ",
"             @26MvzxNzvlbwfpdettttttttttt.c,n&  ",
"             *;16=lsNwwNwgsvslbwwvccc3pcfu<o    ",
"              p;<69BvwwsszslllbBlllllllu<5+     ",
"              OS0y6FBlvvvzvzss,u=Blllj=54       ",
"               c1-699Blvlllllu7k96MMMg4         ",
"               *10y8n6FjvllllB<166668           ",
"                S-kg+>666<M<996-y6n<8*          ",
"                p71=4 m69996kD8Z-66698&&        ",
"                &i0ycm6n4 ogk17,0<6666g         ",
"                 N-k-<>     >=01-kuu666>        ",
"                 ,6ky&      &46-10ul,66,        ",
"                 Ou0<>       o66y<ulw<66&       ",
"                  *kk5       >66By7=xu664       ",
"                   <<M4      466lj<Mxu66o       ",
"                   *>>       +66uv,zN666*       ",
"                              566,xxj669        ",
"                              4666FF666>        ",
"                               >966666M         ",
"                                oM6668+         ",
"                                  *4            ",
"                                                ",
"                                                "
]

import pygtk
pygtk.require('2.0')
import gtk

class Images2Demo(gtk.Window):
    # is invoked when the button is clicked.  It just prints a message.
    def button_clicked(self, widget, data=None):
        print "button %s clicked" % data

    def __init__(self, parent=None):
        gtk.Window.__init__(self)
        try:
            self.set_screen(parent.get_screen())
        except AttributeError:
            self.connect('destroy', lambda *w: gtk.main_quit())

        self.set_title(self.__class__.__name__)
        self.set_border_width(8)
        self.set_border_width(10)

        # a horizontal box to hold the buttons
        hbox = gtk.HBox()

        self.add(hbox)

        # PixbufAnimation
        pixbufanim = gtk.gdk.PixbufAnimation(GOALIE_IMAGE)
        image = gtk.Image()
        image.set_from_animation(pixbufanim)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "1")

        # ImageFromFile
        image = gtk.Image()
        image.set_from_file(REDAPPLE_IMAGE)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "2")

        # ImageFromStockItem
        # The render_icon() method is a convenience method that uses the theme engine and RC file settings for the
        # widget to look up the stock icon specified by stock_id of the specified size and to render it to a pixbuf
        # that is returned. stock_id should be a stock icon ID such as gtk.STOCK_OPEN or gtk.STOCK_OK.
        # size should be one of the GTK Icon Size Constants
        # detail is an optional string that identifies the widget or code doing the rendering, so that theme engines
        # can special-case rendering for that widget or code.

        image = gtk.Image()
        pb = gtk.gdk.Pixbuf
        pb = image.render_icon(gtk.STOCK_HELP, gtk.ICON_SIZE_LARGE_TOOLBAR, None)
        w = pb.get_width()
        h = pb.get_height()
        pb = pb.scale_simple(w*4, h*4, gtk.gdk.INTERP_BILINEAR)
        image.set_from_pixbuf(pb)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "3")

        # ImageFromFile
        image = gtk.Image()
        image.set_from_file(IMPORTANT_IMAGE)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "4")

        # ImageFromPixBuf
        pixbuf = gtk.gdk.pixbuf_new_from_file(SOCCERBALL_IMAGE)
        image = gtk.Image()
        image.set_from_pixbuf(pixbuf)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "5")

        # ImageFromXPM
        self.realize()  # to get the drawable
        # used to determine default values for the new gtk.gdk.Pixmap
        pixmap, mask = gtk.gdk.pixmap_create_from_xpm_d(
            self.window, None, WheelbarrowFull_xpm)
        image = gtk.Image()
        image.set_from_pixmap(pixmap, mask)
        button = gtk.Button()
        button.add(image)
        hbox.pack_start(button)
        button.connect("clicked", self.button_clicked, "6")

        self.show_all()


if __name__ == '__main__':
    Images2Demo()
    gtk.main()


