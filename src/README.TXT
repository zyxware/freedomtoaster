Prerequisites
=============
python
pygtk
pyxml
cdrkit 1.1.1 (or any other cdrecord clone that will burn both CDs and DVDs and have the same output)
cmake (needed to build cdrkit)
libcap (needed to build cdrkit)

Running for the first time
==========================
- Read isolist/README.TXT
- Edit globals.py and maybe change the paths.
- Run main.py from a terminal and descipher the errors.

Running normally
================
Put run.sh in your desktop environment's / window manager's startup list. Do make sure it runs from the directory where main.py is. You may have to write another script that does something like `cd /toasterdir && ./run.sh`

Logging
=======
Please don't delete log.txt on production toasters. Run archiveandclearlog.sh instead.
There is no log parser included yet. If you feel like writing one, please send it to us so we can make it available for everyone to use.

Contact
=======
Please find contact info on the website: http://cdot.senecac.on.ca/projects/toaster/
