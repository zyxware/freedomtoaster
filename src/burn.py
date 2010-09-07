import subprocess
import fcntl
import os
import select
import sys
import re
import time
import gtk
import gobject
import datetime

from globals import *
import log
import main

def burn(button, filename):
    global GBLprocess
    global GBLline
    global GBLoutput
    global GBLtimeStartedBurn
    
    print 'burning ' + filename
    #log.logMessage(MBURNSTART, "'" + filename + "'", "")
    
    showProgressWindow()
    
    # close the 'ready to burn' window
    parentWindow = button.get_parent_window()
    parentWindow.destroy()
    
    #command = BURNINGPROGRAM, 'dev=' + DEVICE, "gracetime=0", "blank=fast"
    command = BURNINGPROGRAM, 'dev=' + DEVICE, 'gracetime=0', '-tao', '-v', '-eject', filename
    
    GBLprocess = subprocess.Popen(command, 0, "wodim", subprocess.PIPE, 
                               subprocess.PIPE, subprocess.STDOUT)
    
    flags = fcntl.fcntl(GBLprocess.stdout, fcntl.F_GETFL)
    fcntl.fcntl(GBLprocess.stdout, fcntl.F_SETFL, flags | os.O_NONBLOCK)
    
    GBLline = ''
    GBLoutput = []
    GBLtimeStartedBurn = datetime.datetime.now()
    
    # have gtk call updateProgress every second
    gobject.timeout_add(1000, updateProgress)
    
# rc is the return code from wodim
def burnFinished(rc):
    global progressWindow
    
    #~ eject()
    
    window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    window.set_default_size(RESOLUTION[0], RESOLUTION[1])
    window.show()
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
    window.connect("key-press-event",on_key_press)
    window.set_destroy_with_parent(True)
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, True, True)
    #fillervbox.set_size_request(-1, 200)
    fillervbox.show()
    
    if rc == 0:
        msg = 'Writing Completed Successfully :-)'
    else:
        msg = 'Writing Failed, Sorry :-('
    
    label = gtk.Label('<span size="36000"><b>' + msg + '</b></span>')
    label.set_use_markup(True)
    label.show()
    vbox.pack_start(label, False, False)
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(-1, 20)
    fillervbox.show()
    
    if rc == 0:
        msg = 'Thank you for using the freedom toaster. In case you need any help\n' + \
              'for installing the software you burned, contact Zyxware or ilug-tvm.'
        log.logMessage(MBURNOK, "", "")
    else:
        msg = 'We apologise for the inconvenience, please contact Zyxware Technologies or Trivandrum GNU/Linux Users Group for assistance.\n'
        log.logMessage(MBURNFAILED, "", "")
    
    label = gtk.Label('<span size="14000">' + msg + '</span>')
    label.set_use_markup(True)
    label.show()
    vbox.pack_start(label, False, False)
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(-1, 20)
    fillervbox.show()
    
    label = gtk.Label('<span size="18000">' + \
                      'The toaster was created by Zyxware Technologies' + \
                      '</span>')
    label.set_use_markup(True)
    label.show()
    vbox.pack_start(label, False, False)
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(-1, 20)
    fillervbox.show()
    
    label = gtk.Label('<span size="18000">' + 'http://freedomtoaster.in' + '</span>')
    label.set_use_markup(True)
    label.show()
    vbox.pack_start(label, False, False)
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(-1, 20)
    fillervbox.show()
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, True, True)
    fillervbox.show()
    
    hbox = gtk.HBox(False, 5)
    vbox.pack_start(hbox, False, False)
    hbox.show()
    
    fillervbox = gtk.VBox(False, 5)
    hbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(100, -1)
    fillervbox.show()
    
    button = gtk.Button()
    button.connect("clicked", closeWindowAndEjectCbk, window)
    button.set_size_request(-1, 100)
    hbox.pack_start(button, True, True)
    button.show()
    button.grab_focus()
    button.connect("focus-in-event",highlightbutton)
    button.connect("key-release-event",highlightbutton)
    label = gtk.Label('<span size="24000"><b>' + 'Press any key to go back to main menu' + '</b></span>')
    label.set_use_markup(True)
    label.show()
    button.add(label)
    
    fillervbox = gtk.VBox(False, 5)
    hbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(100, -1)
    fillervbox.show()
    
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(-1, 20)
    fillervbox.show()
    
    #~ timeLeftLbl.set_text('<span size="24000"><b>' + msg + '</b></span>')
    #~ timeLeftLbl.set_use_markup(True)
    
    closeWindowAndEject(progressWindow)
    
    # close window after timeout passes
    gobject.timeout_add(CLOSEWINDOWTIMEOUT, window.destroy)

def on_key_press(window,event):
    #if gtk.gdk.keyval_name(event.keyval) == "Escape":
    tray_close()
    window.destroy()

def closeWindowAndEject(window):
    window.destroy()
    #~ eject()

def highlightbutton(button,event):
    button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#c3e5ff"))
    
    
def unhighlightbutton(button,event):
    button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))
    
def closeWindowAndEjectCbk(button, window):
    closeWindowAndEject(window)
    
def eject():
    command = 'eject', DEVICE
    subprocess.Popen(command)

def tray_close():
    command = 'eject', '-t', DEVICE
    subprocess.Popen(command, 0, "eject", subprocess.PIPE, subprocess.PIPE, subprocess.STDOUT)


def showProgressWindow():
    global progressWindow
    global timeLeftLbl
    
    progressWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
    progressWindow.set_default_size(RESOLUTION[0], RESOLUTION[1])
    progressWindow.show()
    
    vbox = gtk.VBox(False, 5)
    progressWindow.add(vbox)
    vbox.show()
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, True, True)
    fillervbox.show()
    
    label = gtk.Label('<span size="36000"><b>' + 'Writing Disk' + '</b></span>')
    label.set_use_markup(True)
    label.show()
    vbox.pack_start(label, False, False)
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(-1, 20)
    fillervbox.show()
    
    #~ image = gtk.Image()
    #~ image.set_from_file('images/cd-animated.gif')
    #~ image.show()
    #~ vbox.pack_start(image, False, False)
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(-1, 20)
    fillervbox.show()
    
    label = gtk.Label('<span size="24000"><b>' + 'Time left:' + '</b></span>')
    label.set_use_markup(True)
    label.show()
    vbox.pack_start(label, False, False)
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, False, False)
    fillervbox.set_size_request(-1, 20)
    fillervbox.show()
    
    timeLeftLbl = gtk.Label('<span size="24000"><b>' + 'estimating' + '</b></span>')
    timeLeftLbl.set_use_markup(True)
    timeLeftLbl.show()
    vbox.pack_start(timeLeftLbl, False, False)
    
    fillervbox = gtk.VBox(False, 5)
    vbox.pack_start(fillervbox, True, True)
    fillervbox.show()
    
def updateProgress():
    global GBLprocess
    global GBLline
    global GBLoutput
    
    haveData = True
    while haveData:
        # Check if any data is available from the pipe.
        [i, o, e] = select.select([GBLprocess.stdout], [], [], 0.1)
        if i:
            char = GBLprocess.stdout.read(1)
            
            if char == '':
                if GBLprocess.poll() is None:
                    # process is still running, wait until it dies
                    time.sleep(1)
                    continue
                else:
                    burnFinished(GBLprocess.poll())
                    return False
                
            if char == '\r':
                # replace carriage return with newline
                char = '\n'
            
            if not char == '\b':
                # ignore backspace
                GBLline += char
            
            if char == '\n':
                #sys.stdout.write(GBLline)
                log.logWodim(GBLline)
                
                # save the GBLline
                GBLoutput.append(GBLline)
                
                # check if this is a progress line
                if re.match('^Track', GBLline):
                    estimateTimeLeft(GBLline)
                
                GBLline = ''
                
                if re.compile("Re-load disk and hit <CR>").match(GBLoutput[-1]):
                    # wodim is asking me to press enter
                    GBLprocess.stdin.write("\n")
        else:
            print 'no data'
            haveData = False
    
    # poll() will return the process's return code if it dies
    # or None if it's still running.
    if not GBLprocess.poll() is None:
        burnFinished(GBLprocess.poll())
        return False
    
    return True

def estimateTimeLeft(line):
    global timeLeftLbl
    global GBLtimeStartedBurn
    
    # line looks like 'Track 01:   92 of  120 MB written (fifo  98%) [buf  92%]   4.2x.\n'
    megsWritten = re.findall('\s+(\d+) of', line)
    
    # line not in proper format
    if len(megsWritten) == 0 or int(megsWritten[0]) == 0:
        return
    
    # won't get a good estimate until wrote at least 10 M
    if int(megsWritten[0]) < 15:
        return
    
    timeNow = datetime.datetime.now()
    
    # can't calculate speed
    if timeNow == GBLtimeStartedBurn:
        return
    
    totalMegs = re.findall(' of\s+(\d+)', line)
    
    # line not in proper format
    if len(totalMegs) == 0:
        return
    
    timeLeft = (timeNow - GBLtimeStartedBurn).seconds * (int(totalMegs[0]) - int(megsWritten[0])) / \
               int(megsWritten[0])
    
    # 30 seconds for fixating and such
    timeLeft += 30
    
    print timeLeft, 's left', timeLeft / 60 + 1, 'm left'
    
    if timeLeft / 60 + 1 > 1:
        timeLeftLbl.set_text('<span size="24000"><b>' + str(timeLeft / 60 + 1) + ' minutes' + '</b></span>')
    else:
        timeLeftLbl.set_text('<span size="24000"><b>' 'less than one minute' + '</b></span>')
    timeLeftLbl.set_use_markup(True)
