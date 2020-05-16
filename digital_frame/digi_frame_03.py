#!/usr/bin/env python
#
# To make executable: chmod +x this_file.py
# To execute: ./this_file.py
#
# Project: Digi Picture Frame
# Author:  Mike Calyer
# Date:    05/2013
#
# Display jpg pictures , determines orientation and rotates picture frame
# to align
#
# Constrants:
#  1. Picutre size = 1824 x 1216
#  2. Exif orientation field must be vaild

import os
import pygame 
import time
import random
import sys
from   motor       import *
from   exif_orient import *
from   usb_drive   import *

# ---------------------------------------------------------------------------
#  Digi Frame
# ---------------------------------------------------------------------------



#Initialize file list
file_list = []

# Initialize Motor State = OFF
motor_control(MOTOR_OFF)

# Initilaize
pygame.init()

# Look for USB drive plugged in
if usb_drive_detect():    
    pygame.quit()
    exit()
    
# Get files on USB drive 
path,files = usb_drive_files()
if not files:
    pygame.quit()
    exit()

# Look for jpg files with exif orient                 
for file in files:
    file = path + "/" + file
    # Get jpg image list with valid exif orientation
    if file.endswith(".jpg") or file.endswith(".JPG"):
        #Get orientation
        if 'ERROR'!= Exif_Orientation(file,0):             
            file_list.append(file)

# If no jpg files with orient exif 
if not file_list:
    print"No jpg files found\n"  
    pygame.quit()
    exit()

# Create random picture list
random.shuffle(file_list)

# List picture list and orientation
i = 0
for picture in file_list:
    orient = Exif_Orientation(picture)
    print"Picture:  %s , Orientation: %s \n" % (file_list[i] , orient)
    i = i + 1
pygame.time.wait(3000)

# Make mouse not visable
pygame.mouse.set_visible(False)

# Create Simple Window
background_color = (255,255,255)
#(width,height) = (1824,984)
(width,height) = (1920,1080)
screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)



# Load picture from picture list
for picture in file_list:
    orient = Exif_Orientation(picture)
            
    image  = pygame.image.load(picture).convert()
    #image  = pygame.transform.scale(image,(1824,1216))
    image  = pygame.transform.scale(image,(1920,1280))
    
    # Put on screen
    #screen.blit(image,(0,-232))
    screen.blit(image,(0,-100))
    pygame.display.flip()

    
    #Rotate frame if necessary
    print" Rotate Picture : %s %s \n" % (picture,orient)    
    position = rotate(orient)
    if 'ROTATE_ERROR' == position:
        print" Rotate Picture Failure\n"
        pygame.quit()
        exit()
            
    
    # Show picture for X seconds
    pygame.time.wait(1000 * 6)



#Exit
    
if 'CW_90' == position:
    position = rotate('ZERO')

    
pygame.time.wait(1000)
pygame.quit()



