# width, height
RESOLUTION = 1024,768

# Directory containing the xml files describing the available isos.
# (these can be symbolic links to another directory)
HOMEDIR = '/home/zyxware/freedomtoaster'

ISOLISTDIR = HOMEDIR + '/src/isolist/'
# Where on the filesystem the ISOs are
ISOPATH = HOMEDIR + '/src/iso/'

#sym links to 12 isos to be displayed on home screen
HOMESCREEN = HOMEDIR + '/src/homescreen/'


# Where on the filesystem the images (to be used inside buttons) are
ISOIMAGEPATH = ISOPATH
# The file with the help, including path
HELPFILE = HOMEDIR + "/src/help.txt"

# More stuff directory
MORESTUFF = HOMEDIR + '/src/morestuff/'

# Any more than this in ISOLISTDIR will be ignored
MAXNUMISOS = 6

# Program to do the burning: wodim or cdrecord or any other compatible app
BURNINGPROGRAM = 'wodim'

# Recorder
#DEVICE = '/dev/hda'
DEVICE = '/dev/scd0'
#DEVICE = '/dev/sr0'

# How long a window like 'iso info' or 'help' will stay up 
# until it is closed automatically (milliseconds)
# 10 minutes (600 seconds) should be good
CLOSEWINDOWTIMEOUT = 600000

# Log file to write to, including file
LOGFILE = HOMEDIR + '/src/log.txt'

# This list is here so whomever is writing a parser for the log
# file knows what the messages can be.
# Please call the log functions with the messageName from this list.
# Add a message here if you need a new one.
MTOASTERSTART = 'TOASTERSTART' # program started
MTOASTEREND = 'TOASTEREND'     # program exited properly (unlikely to happen)
MISOINFO = 'ISOINFO'           # pressed the button for an iso (not requested burn)
MHELPSCREEN = 'HELPSCREEN'     # pressed the help button
MMORESTUFF = 'MORESTUFF'       # pressed the more stuff buttonMBURNSTART = 'BURNSTART'       # pressed the buttonto start burning
MBURNOK = 'BURNOK'             # burn completed successfully (according to wodim)
MBURNFAILED = 'BURNFAILED'     # burn failed (according to wodim)
MWODIM = 'WODIM: '             # one line of the stdout/stderr from wodim

