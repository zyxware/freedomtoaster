#!/usr/bin/python

# this file is not part of the toaster program, it's an independent script

import os

os.execl('/usr/local/bin/wodim', 'wodim', 'dev=/dev/sr0', 'gracetime=0', 'blank=fast')

