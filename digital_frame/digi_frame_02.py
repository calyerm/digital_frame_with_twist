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
import RPi.GPIO as GPIO

def Exif_Orientation(name,debug = 0):
    
    #Initialize
    ORIENTATION_TAG = 0x0112  
    endian_flag     = 0    
    
    # Get multibyte integer from little/big endian format
    def interger_endian(str , endian_flag):
        x = 0
        y = 0
    
        if endian_flag: 
            # Little endian   (Motorola)
            for c in str:
                x = (x << 8) | ord(c)        
        else:
            # Big endian (Intel)
            for c in str:
                x = x | (ord(c) << y)
                y = y + 8
            
        return x
    
    # If debug mode , print     
    def debug_print(str):   
        print(str)    
    if not debug:
        def debug_print(str):
            pass

    debug_print(('Picture: %s \n' % name))
            
    #Open file
    try:
        file = open(name, 'rb')    
        data = file.read(16)                
    except:
        # Can not read file    
        debug_print(('Can not open or read file\n'))          
        return -1   
    

    
    #Check for jpeg SOI    
    if data[0:2] != '\xFF\xD8':       
        file.close()
        debug_print(('Check for SOI failed\n'))   
        return -2 

    #Check for APP0 or APP1 markers , if found determine Exif offset    
    if data[2:4] == '\xFF\xE0':
        # Get Exif Offset
        # Offset     = APP0 size + APP0 tag size + SOI tag size
        Exif_Offset  = (ord(data[4])*256+ord(data[5])) + 2 + 2     
    elif data[2:4] == '\xFF\xE1':
        Exif_Offset = 2
    else:
        file.close()
        debug_print(('Check for APP0 markers or APP1 markers failed\n'))   
        return -2   
    
    
    #Get Exif data , usually the ORIENTATION_TAG can be found in first 256 bytes 
    file.seek(Exif_Offset)
    data = file.read(512)
    
    #Check for APP1 Marker and Exif ID
    if data[0:2] != '\xFF\xE1' or data[4:10] != 'Exif\x00\x00':
       file.close()
       debug_print(('Check for APP1 Marker or Exif ID failed\n'))   
       return -3 
       
    #Get endian flag    
    if data[10:12] == 'II':
        endian_flag = 0
    elif data[10:12] == 'MM':
        endian_flag = 1    
    else:        
        file.close()
        debug_print(('Could not determine endian type , failure\n'))   
        return -4     
           
    #Get offset to first IFD , this is usually = 8 , from begining of TIFF header , so next byte after TIFF IFD offset
    # Not used
    # IFD_OFFSET = interger_endian(data[14:18] , endian_flag)      
    
    #Get IFD Number of directory entries , 2 bytes , first group of IFD 
    # Usually the ORIENTATION_TAG can be found in first IFD group , so only looking in first group
    IFD_NUMBER_DIRECTORY_ENTRIES = interger_endian(data[18:20] , endian_flag)    
   
    #Get first IFD , assume's IIFD offset of 8 bytes
    IFD_OFFSET = 20
    IFD_SIZE   = 12  
    
    # Find ORIENTATION_TAG 
    for i in range(0,IFD_NUMBER_DIRECTORY_ENTRIES):
        TAG = interger_endian(data[IFD_OFFSET:(IFD_OFFSET + 2)] , endian_flag) 
        debug_print(('TAG: %x \n' %  TAG))
        if ORIENTATION_TAG == TAG:            
            IFD_VALUE_OFFSET =  IFD_OFFSET + 8 
            value = interger_endian(data[IFD_VALUE_OFFSET:(IFD_VALUE_OFFSET + 2)] , endian_flag)
            debug_print(('Orientation: %d \n' %  value)) 
            file.close()           
            return value
        IFD_OFFSET = IFD_OFFSET + IFD_SIZE    
        
    # Can not find orientation 
    file.close()
    debug_print(('Could not find Orientation tag\n')) 
    return -5 



#Initialize Motor Control GPIO
gpio_motor_Eable = 25
gpio_motor_L1    = 26
gpio_motor_L2    = 27
gpio_motor_limit_switch = 28
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_motor_Enable,GPIO.OUT)
GPIO.setup(gpio_motor_L1,GPIO.OUT)
GPIO.setup(gpio_motor_L2,GPIO.OUT)
GPIO.setup(gpio_motor_limit_switch,GPIO.IN)

# Rotate_GPIO_Decode: 
# Motor Direction:
# Forward or CW   En = 1 , L1 = 0 , L2 = 1
# Backward or CCW En = 1 , L1 = 1 , L2 = 0
# Brake           En = 1 , L1 = 0 , L2 = 0
# Off             En = 0 , L1 = X , L2 = X
rotate_GPIO_Decode = {   0 : [0,0,0]  ,
                         1 : [0,0,0]  ,
                         8 : [1,1,0]  ,
                         6 : [1,0,1]  } 
#Initilaize
pygame.init()

#Look for USB drive plugged in
file_list = []
m_list    = os.listdir("//media")
if not m_list:
    print"No USB Drive plugged in\n"  
    pygame.quit()
    exit()
    
path      = "//media/" + m_list[0]
files     = os.listdir("//media/" + m_list[0])
for file in files:
    file = path + "/" + file
    # Get jpg image list with valid exif orientation
    if file.endswith(".jpg") or file.endswith("JPG"):        
        if 0 < Exif_Orientation(file,1):             
            file_list.append(file)

if not file_list:
    print"No picture files found\n"  
    pygame.quit()
    exit()

# Create random picture list
random.shuffle(file_list)

# List picture list and orientation
i = 0
for picture in file_list:
    orient = Exif_Orientation(picture)
    print"Picture:  %s , Orientation: %d \n" % (file_list[i] , orient)
    i = i + 1
pygame.time.wait(3000)

#Make mouse not visable
pygame.mouse.set_visible(False)

# Create Simple Window
background_color = (255,255,255)
(width,height) = (1824,984)
screen = pygame.display.set_mode((width,height),pygame.FULLSCREEN)

#Window background color
#screen.fill(background_color)

#Window caption
#pygame.display.set_caption('Move Frame 05/05/2013')



#Load picture from picture list
for picture in file_list:
    image = pygame.image.load(picture).convert()
    image = pygame.transform.scale(image,(1824,1216))
    w = image.get_width()
    h = image.get_height()
    # Put on screen
    screen.blit(image,(0,-232))
    pygame.display.flip()
    #Rotate frame if necessary code here !!
    pygame.time.wait(10000)



#Exit
pygame.time.wait(1000)
print"x:  %d y:  %d \n" % (w,h)  
pygame.quit()



