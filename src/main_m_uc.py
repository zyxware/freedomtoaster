#!/usr/bin/python

import gtk
import gobject

from globals import *
import sys
sys.path.append("/usr/lib/python%s/site-packages/oldxml"% sys.version[:3])

import isolist
import burn
import log
import morestuff

clickflag = 0

class ToasterMain:
    
    def destroy(self, widget, data=None):
        print "quitting"
        log.logMessage(MTOASTEREND, "", "")
        gtk.main_quit()
    
    def __init__(self):
	gtk.gdk.
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", self.destroy)
        self.window.set_default_size(RESOLUTION[0], RESOLUTION[1])
        self.window.show()
        
        mainvbox = gtk.VBox(False, 20)
        self.window.add(mainvbox)
        mainvbox.show()
        
        vscrollbar = gtk.VScrollbar(adjustment=None)

	#gap
        fillerhbox = gtk.HBox(True, 0)
        fillerhbox.set_size_request(-1,20)
        fillerhbox.show()
        mainvbox.pack_start(fillerhbox,False,False)

        # top middle (title)
        titleLbl = gtk.Label('<span size="33000"><span color="#2c089c"><b><span face="good times">' + 'Zyx' + '</span></b></span></span>' + '<span size="33000" color="#8634e0" face="good times"><b>' + 'ware' + '</b></span>')
	mainlbl = gtk.Label('<span size="37000"><span face="good times"><b>' + 'FREEDOM TOASTER' + '</b></span></span>')
	mainlbl.set_use_markup(True)
	mainlbl.show()
        titleLbl.set_use_markup(True)
        mainvbox.pack_start(titleLbl, False, False)
	mainvbox.pack_start(mainlbl, False, False)
        titleLbl.show()
        directionsLbl = gtk.Label('<span size="12000">' + 
                                  "Choose the distro you want using the navigational keys and press enter" + 
                                  '</span>')
        directionsLbl.set_use_markup(True)
        mainvbox.pack_start(directionsLbl, False, False)
        directionsLbl.show()
        
        # load the list of available software
        isoList = isolist.populateIsoList()
        #isonum = isolist.retnumisos()
        numButtonsAdded = 0
        for iso in isoList:
            # Use this condition if you want two buttons per row:
            if numButtonsAdded % 3 == 0:
            # Use this condition if you want one button per row:
            #if numButtonsAdded % 2 == 0 or numButtonsAdded % 2 == 1:
                hbox = gtk.HBox(False, 5)
                mainvbox.pack_start(hbox)
                hbox.show()
            
            # button for this software
            button = gtk.Button()
            button.connect("focus-in-event",highlightbutton)
 	    button.connect("key-release-event",highlightbutton)
            button.connect("key-press-event",unhighlightbutton)
            button.connect("clicked", readyToBurnScreen, iso)
            hbox.pack_start(button, True, True)
            button.set_size_request(25,25)          
            button.show()
            
            # This is unfortunately needed because the text in a label will not
            # wrap to the size of the parent widget so I have to resize the label 
            # manually.
            # Set the value depending on how many buttons per row you have and 
            # the size of the image.
            # For a 1024x768 window:
            # - with one column and 100px buttons: 850
            # - with two columns and 100px buttons: 350
            buttonTextWidth = 25
            populateButton(button, iso, buttonTextWidth)
            
            numButtonsAdded += 1
        
        # More stuff button
        button = gtk.Button()
        button.connect("clicked", moreStuff)
	button.connect("focus-in-event",highlightbutton)
	button.connect("key-release-event",highlightbutton)	
        button.connect("key-press-event",unhighlightbutton)
        mainvbox.pack_start(button, True, True)
        button.show()
        
        # More stuff button contents
        label = gtk.Label('<span size="20000"><b>More stuff</b></span>')
        label.set_use_markup(True)
        label.show()
        button.add(label)
        
        #get rid of the mouse cursor
        toaster_display = gtk.gdk.display_get_default()
	toaster_screen = toaster_display.get_default_screen()
	toaster_display.warp_pointer(toaster_screen,toaster_screen.get_width()+2,toaster_screen.get_height()+2)
	log.logMessage(MTOASTERSTART, "", "")
       
    def main(self):
        gtk.main()

def highlightbutton(button,event):
    button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#c3e5ff"))
    
    
def unhighlightbutton(button,event):
    button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
    
    
def populateButton(button, iso, buttonTextWidth):
    hbox = gtk.HBox(False, 5)
    hbox.show()
    button.add(hbox)
    
    # picture
    image = gtk.Image()
    image.set_from_file(iso.picture)
    image.show()
    hbox.pack_start(image, False, False)
    
    # box for the name and description
    vbox = gtk.VBox(False, 5)
    vbox.show()
    hbox.pack_start(vbox, True, True)
    
     #iso name
    label = gtk.Label('<span size="15000"><b>' + iso.displayname + '</b></span>')
    label.set_use_markup(True)
    label.show()
    vbox.pack_start(label, True, True)
    
    return vbox, label
    
def readyToBurnScreen(button, iso):
    log.logMessage(MISOINFO, "'" + iso.displayname + "'", "'" + iso.filename + "'")
    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_default_size(RESOLUTION[0], RESOLUTION[1])
    window.show()
    window.connect("key-press-event",on_key_press)
    hbox = gtk.HBox(False, 5)
    mainvbox = gtk.VBox(False, 20)
    window.add(hbox)
    hbox.show()

    # padding on the left
    fillervbox = gtk.VBox(False, 5)
    fillervbox.set_size_request(100, -1)
    hbox.pack_start(fillervbox, False, False)
    fillervbox.show()
    
    # all content goes here
    vbox = gtk.VBox(False, 5)
    hbox.pack_start(vbox, True, True)
    vbox.show()
    
    # padding on the right
    fillervbox = gtk.VBox(False, 5)
    fillervbox.set_size_request(100, -1)
    hbox.pack_start(fillervbox, False, False)
    fillervbox.show()
    
    #Horizontal padding
    fillerhbox = gtk.HBox(False, 5)
    fillerhbox.set_size_request(-1,20)
    vbox.pack_start(fillerhbox, False, False)
    fillerhbox.show()
    
    # iso name
    label = gtk.Label('<span size="36000"><b>' + iso.displayname + '</b></span>')
    label.set_use_markup(True)
    label.show()
    vbox.pack_start(label, False, False)
    
    #Horizontal padding
    fillerhbox = gtk.HBox(False, 5)
    fillerhbox.set_size_request(-1,20)
    vbox.pack_start(fillerhbox, False, False)
    fillerhbox.show()
    
    # box for iso picture and description
    hbox = gtk.HBox(False, 5)
    vbox.pack_start(hbox, False, False)
    hbox.show()
    
    # picture
    image = gtk.Image()
    image.set_from_file(iso.picture)
    image.show()
    hbox.pack_start(image, True, True)
    
    # iso description
    label = gtk.Label('<span size="12000">' + iso.longdescription + '</span>')
    label.set_use_markup(True)
    label.set_line_wrap(True)
    label.set_size_request(RESOLUTION[0] - 400, -1)
    label.show()
    hbox.pack_start(label, False, False)
    
    #Horizontal padding
    fillerhbox = gtk.HBox(False, 5)
    fillerhbox.set_size_request(-1,20)
    vbox.pack_start(fillerhbox, False, False)
    fillerhbox.show()
    
    if iso.type == 'CD':
        label = gtk.Label('<span size="24000"><b>Blank CD or DVD required</b></span>')
    else:
        label = gtk.Label('<span size="24000"><b>Blank DVD required</b></span>')
    label.set_use_markup(True)
    label.show()
    vbox.pack_start(label, False, False)
    
    #Horizontal padding
    fillerhbox = gtk.HBox(False, 5)
    fillerhbox.set_size_request(-1,20)
    vbox.pack_start(fillerhbox, False, False)
    fillerhbox.show()
    
    button = gtk.Button()
    button.connect("clicked", burn.burn, iso.filename)
    button.connect("focus-in-event",highlightbutton)
    button.connect("key-press-event",highlightbutton)
    button.set_size_request(-1, 100)
    vbox.pack_start(button, False, False)
    button.show()
    label = gtk.Label('<span size="24000"><b>' + 'Insert disk and press here to burn' + '</b></span>')
    label.set_use_markup(True)
    label.show()
    button.add(label)
    button.grab_focus()
    
    #Horizontal padding
    fillerhbox = gtk.HBox(False, 5)
    fillerhbox.set_size_request(-1,20)
    vbox.pack_start(fillerhbox, False, False)
    fillerhbox.show()

    
    
    # close window after timeout passes
    gobject.timeout_add(CLOSEWINDOWTIMEOUT, window.destroy)

def moreStuff(button):
    log.logMessage(MMORESTUFF, "", "")
    morestufflist = morestuff.populateIsoList()

    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_default_size(RESOLUTION[0], RESOLUTION[1])
    window.connect("key-press-event",on_key_press)
    window.set_flags(gtk.CAN_FOCUS)
    window.show()
    
    # main container that contains the control
    vbox = gtk.VBox(False, 5)
    window.add(vbox)
    vbox.show()

    #gap
    fillerhbox = gtk.HBox(True, 0)
    fillerhbox.set_size_request(-1,20)
    fillerhbox.show()
    vbox.pack_start(fillerhbox,False,False)
	
    titleLbl = gtk.Label('<span size="33000"><span color="#2c089c"><b><span face="good times">' + 'Zyx' + '</span></b></span></span>' + '<span size="33000" color="#8634e0" face="good times"><b>' + 'ware' + '</b></span>')
    mainlbl = gtk.Label('<span size="37000"><span face="good times"><b>' + 'FREEDOM TOASTER' + '</b></span></span>')
    mainlbl.set_use_markup(True)
    mainlbl.show()
    titleLbl.set_use_markup(True)    
    vbox.pack_start(titleLbl, False, False)
    vbox.pack_start(mainlbl, False, False)
    titleLbl.show()
    
    # padding on the top
    fillerhbox = gtk.HBox(False, 5)
    fillerhbox.set_size_request(-1, 5)
    vbox.pack_start(fillerhbox, False, False)
    #fillerhbox.show()
    
    # listbox control with list of isos
    listStore = gtk.ListStore(str, gtk.gdk.Pixbuf)
    for iso in morestufflist:
        listStore.append([iso.displayname, gtk.gdk.pixbuf_new_from_file(iso.picture)])
        
    listColumn = gtk.TreeViewColumn()
    iconRenderer = gtk.CellRendererPixbuf()
    #iconRenderer.height = 125
    iconRenderer.set_fixed_size(125,125)
    textRenderer = gtk.CellRendererText()
    textRenderer.set_property("scale", 3)
    textRenderer.set_property("scale-set", "True")
    listColumn.pack_start(iconRenderer, True)
    listColumn.set_attributes(iconRenderer, pixbuf = 1)
    listColumn.pack_start(textRenderer, True)
    listColumn.set_attributes(textRenderer, text = 0)
    
    listBox = gtk.TreeView(listStore)
    listBox.append_column(listColumn)
    
    listBox.connect("row-activated", onlistBoxSelect)
    #listBox.connect("key-press-event",on_key_press)

    scrolledwindow = gtk.ScrolledWindow()
    scrolledwindow.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
    vbox.pack_start(scrolledwindow, True, True)
    scrolledwindow.show()
    scrolledwindow.add(listBox)
    #hbox = gtk.HBox(False, 5)
    #hbox.set_size_request(-1, 200)
    #hbox.pack_start(listBox, False, False)
    #vbox.pack_start(hbox, True, True)
    #hbox.show()
    listBox.show()

    # padding on the bottom
    fillerhbox = gtk.HBox(False, 5)
    fillerhbox.set_size_request(-1, 20)
    vbox.pack_start(fillerhbox, False, False)
    fillerhbox.show()

    # back button
    #backbutton = gtk.Button()
    #backbutton.connect("clicked", closeWindowCbk, window)
    #backbutton.set_size_request(-1, 100)
    #vbox.pack_start(backbutton, False, False)
    #backbutton.show()
    
    # back button contents
    #label = gtk.Label('<span size="24000"><b>' + 'Press here to go to the main menu' + '</b></span>')
    #label.set_use_markup(True)
    #label.show()
    #backbutton.add(label)

# The callback function: 
# focusme is the widget that will be focused
def on_key_press(window,event):
    if gtk.gdk.keyval_name(event.keyval) == "Escape":
        window.destroy()
        
             

def timeoutFocus(widget, focusme):
   gobject.timeout_add(10, lambda: focusme.grab_focus())

    
def goToBurnButton(widget, direction, burnbutton):
    burnbutton.grab_focus()
    #the treeview control was gaining focus back because of the order
    #of the order of nav-fail and unknown event :)
    gobject.timeout_add(10, lambda: burnbutton.grab_focus())

def onlistBoxSelect(treeview, path, view_column):
    #name=treeview.get_column(0)
    #showMessage(str(path.__class__))
    model = treeview.get_model()
    value1=model.get(model.get_iter(path),0)
    #showMessage(str(model.get(model.get_iter(path),0)))
    morestufflist=morestuff.populateIsoList()
    for iso in morestufflist:
        if iso.displayname == value1[0]:
            readyToBurnScreen(None, iso)
            
    
    

def showMessage(string):
    message = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_NONE, string)
    message.add_button(gtk.STOCK_QUIT, gtk.RESPONSE_CLOSE)
    resp = message.run()
    if resp == gtk.RESPONSE_CLOSE:
        message.destroy()


def helpScreen(button):
    log.logMessage(MHELPSCREEN, "", "")
    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_default_size(RESOLUTION[0], RESOLUTION[1])
    window.show()
    
    hbox = gtk.HBox(False, 5)
    window.add(hbox)
    hbox.show()
    
    # padding on the left
    fillervbox = gtk.VBox(False, 5)
    fillervbox.set_size_request(50, -1)
    hbox.pack_start(fillervbox, False, False)
    fillervbox.show()
    
    # all content goes here
    vbox = gtk.VBox(False, 5)
    hbox.pack_start(vbox, True, True)
    vbox.show()
    
    # padding on the right
    fillervbox = gtk.VBox(False, 5)
    fillervbox.set_size_request(50, -1)
    hbox.pack_start(fillervbox, False, False)
    fillervbox.show()
    
    # BEGIN HELP contents
    helpfile = open(HELPFILE, "r")
    helptext = helpfile.read()
    
    label = gtk.Label(helptext)
    label.set_use_markup(True)
    label.set_size_request(RESOLUTION[0] - 200, -1)
    label.set_line_wrap(True)
    label.show()
    vbox.pack_start(label, False, False)
    # END HELP contents
    
    #~ # padding between help and close button
    #~ fillervbox = gtk.VBox()
    #~ vbox.pack_start(fillervbox, True, True)
    #~ fillervbox.show()
    
    # close button
    button = gtk.Button()
    button.connect("clicked", closeWindowCbk, window)
    button.set_size_request(-1, 100)
    vbox.pack_start(button, False, False)
    button.show()
    
    # close button contents
    label = gtk.Label('<span size="24000"><b>' + 'Press here to go to the main menu' + '</b></span>')
    label.set_use_markup(True)
    label.show()
    button.add(label)
    
    # close window after timeout passes
    gobject.timeout_add(CLOSEWINDOWTIMEOUT, window.destroy)

def closeWindowCbk(button, window):
    window.destroy()

if __name__ == "__main__":
    main = ToasterMain()
    main.main()
