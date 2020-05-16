# Name: usb_drive.py
# Description: Digi Frame USB drive functions
# Date: 06/13/2013
# Author: M.Calyer


import sys
import os
import sys

# Look for USB drive plugged in 
def usb_drive_detect():    
    m_list = os.listdir("//media")
    if not m_list:
        return 1
    return 0

# Return USB file list and path
def usb_drive_files():
    path   = []
    files  = []
    m_list = []
    m_list = os.listdir("//media")
    if not m_list:
        return[path,files]
    path   = "//media/" + m_list[0]     
    files  = os.listdir("//media/" + m_list[0])      
    return[path,files]


if __name__ == '__main__':
     
    # See if US drive is plugged in
    if usb_drive_detect():
        print "USB drive Not Plugged In !\n"
        exit()

    # USB Drive plugged in   
    print "USB drive Plugged In !\n"
        
    # Get USB drive files
    path,files = usb_drive_files()
    if not files:
        print "USB drive plugged in , no files found\n"
    
    # Look got jpg files on USB drive                 
    for file in files:
        file = path + "/" + file
        # Get jpg image list with valid exif orientation
        if file.endswith(".jpg") or file.endswith(".JPG"):
            # Print file Get orientation
            print" %s \n" % file
            exit()
              
    
    
