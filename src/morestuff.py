import os
import re
from xml.dom.ext.reader import Sax2
from xml.dom.NodeFilter import NodeFilter
from xml.dom import minidom, Node
import gtk

from globals import *

numIsos = 0
class Iso:
    def __init__(self):
        self.displayname = ''
        self.category = ''
        self.description = ''
        self.longdescription = ''
        self.picture = ''
        self.filename = ''
        self.type = ''    

def populateIsoList():
    
    
    numIsos = 0          
    isoList = []
    
    filelist = os.listdir(MORESTUFF)
    filelist.sort()
    
    # for every file in the directory
    for filename in filelist:
        #~ print filename
        # find xml files
        if re.search('\.xml$', filename):
            
            # data about this iso will be stored in here:
            iso = Iso()
            
            # read the xml file
            reader = Sax2.Reader()
            doc = reader.fromStream('file://' + MORESTUFF + filename)
            
            for node in doc.documentElement.childNodes:
                if node.nodeType == Node.ELEMENT_NODE:
                    
                    #~ print node.nodeName + ' -> ' + node.firstChild.nodeValue
                    
                    if node.firstChild:
                        nodeValue = node.firstChild.nodeValue
                    else:
                        # this happens for an empty tag
                        continue
                    
                    if node.nodeName == 'displayname':
                        iso.displayname = nodeValue
                    elif node.nodeName == 'category':
                        iso.category = nodeValue
                    elif node.nodeName == 'description':
                        iso.description = nodeValue
                    elif node.nodeName == 'longdescription':
                        iso.longdescription = nodeValue
                    elif node.nodeName == 'picture':
                        iso.picture = ISOIMAGEPATH + nodeValue
                    elif node.nodeName == 'filename':
                        iso.filename = ISOPATH + nodeValue
                    elif node.nodeName == 'type':
                        iso.type = nodeValue
                    
            isoList.append(iso)
            numIsos += 1
        
        if numIsos >= 100:
            break
            
    return isoList

def retnumisos():
           return numIsos
