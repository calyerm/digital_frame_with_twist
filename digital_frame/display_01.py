import os
import pygame
import time
import random

    
   
disp_no = os.getenv("DISPLAY")
if disp_no:
    print "I'm running under X display = {0}".format(disp_no)
        
# Check which frame buffer drivers are available
# Start with fbcon since directfb hangs with composite output
drivers = ['fbcon', 'directfb', 'svgalib']
found = False
for driver in drivers:
    # Make sure that SDL_VIDEODRIVER is set
    if not os.getenv('SDL_VIDEODRIVER'):
        os.putenv('SDL_VIDEODRIVER', driver)
    try:
        pygame.display.init()
    except pygame.error:
        print 'Driver: {0} failed.'.format(driver)
        continue
    found = True
    break
    
if not found:
    raise Exception('No suitable video driver found!')
     
# Get display size  
size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
print "Framebuffer size: %d x %d" % (size[0], size[1])


# Set video mode 
#self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        
# Clear the screen to start
#self.screen.fill((0, 0, 0))    
    
# Initialise font support
#pygame.font.init()

# Render the screen
#pygame.display.update()

 