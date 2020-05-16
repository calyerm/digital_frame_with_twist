import os
import sys


# ------------------------------------------------------------------------
# JPG File
# ------------------------------------------------------------------------

# Exif_Orientation: Reads JPG Exif orientation info
# Returns value of orientation or ERROR
# 
# Orientation Values:
#   0 = None                          , returns INVALID
#   1 = Landscape , no rotate needed  , returns ZERO
#   3 = Needs to be rotated CCW  180  , returns CCW_180
#   6 = Needs to be rotated CW    90  , returns CW_90
#   8 = Needs to be rotated CCW   90  , returns CCW_90

# Error Returns ERROR
# Error sources
#   Can not read jpg file
#   Can not find JPG SOI
#   Can not find APP0 or APP1
#   Can not find Exif ID
#   Can not determine endian type
#   Can not find orient TAG

def Exif_Orientation(name,debug = 0):
    

    ORIENT_ROTATE_DECODE =  {   0 : 'INVALID'  ,
                                1 : 'ZERO'     ,
                                3 : 'CCW_180'  ,
                                6 : 'CW_90'    ,
                                8 : 'CCW_90'   }
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
        return 'ERROR'   
    
    
    #Check for jpeg SOI    
    if data[0:2] != '\xFF\xD8':       
        file.close()
        debug_print(('Check for SOI failed\n'))   
        return 'ERROR' 

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
        return 'ERROR'   
    
    
    #Get Exif data , usually the ORIENTATION_TAG can be found in first 256 bytes 
    file.seek(Exif_Offset)
    data = file.read(512)
    
    #Check for APP1 Marker and Exif ID
    if data[0:2] != '\xFF\xE1' or data[4:10] != 'Exif\x00\x00':
       file.close()
       debug_print(('Check for APP1 Marker or Exif ID failed\n'))   
       return 'ERROR' 
       
    #Get endian flag    
    if data[10:12] == 'II':
        endian_flag = 0
    elif data[10:12] == 'MM':
        endian_flag = 1    
    else:        
        file.close()
        debug_print(('Could not determine endian type , failure\n'))   
        return 'ERROR'      
           
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
            # Decode JPG orient value to rotate value            
            if value not in ORIENT_ROTATE_DECODE:
                value = 0
            return ORIENT_ROTATE_DECODE[value]
        
        IFD_OFFSET = IFD_OFFSET + IFD_SIZE    
        
    # Can not find orientation 
    file.close()
    debug_print(('Could not find Orientation tag\n')) 
    return 'ERROR'  
