# -------------------------------------------------------------------------------------------
# Motor
# -------------------------------------------------------------------------------------------
import os
import time
import RPi.GPIO as GPIO

# Motor Control GPIO
# Rotate_GPIO_Decode: 
# Motor Direction:
# Forward or CW   En = 1 , L1 = 0 , L2 = 1
# Backward or CCW En = 1 , L1 = 1 , L2 = 0
# Brake           En = 1 , L1 = 0 , L2 = 0
# Off             En = 0 , L1 = X , L2 = X

# Motor GPIO Decode
MOTOR_OFF   =  [GPIO.LOW  ,GPIO.LOW,  GPIO.LOW ]
MOTOR_CW    =  [GPIO.HIGH ,GPIO.HIGH, GPIO.LOW ]
MOTOR_CCW   =  [GPIO.HIGH ,GPIO.LOW,  GPIO.HIGH]
MOTOR_BRAKE =  [GPIO.HIGH ,GPIO.LOW,  GPIO.LOW ]
MOTOR_TEST  =  [GPIO.HIGH ,GPIO.HIGH, GPIO.HIGH]

# Global Motor state
motor_state            = MOTOR_OFF
current_motor_position = 'ZERO'                         
next_motor_position    = 'ZERO'


#  Motor Sequence Table
#  [Current Motor Position,Next Motor Position] -> Motor action required           
#                       Motor Position 
#                        Current       Next          Motor Control
MOTOR_ROTATE_SEQ =  {  ('ZER0'      , 'ZERO'   )   : MOTOR_OFF ,
                       ('CW_90'     , 'CW_90'  )   : MOTOR_OFF ,    
                       ('ZERO'      , 'CW_90'  )   : MOTOR_CW  ,
                       ('CW_90'     , 'ZERO'   )   : MOTOR_CCW }
                                          
                       
                           
# Configure Motor GPIO Pin Usage
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
gpio_motor_Enable = 25
gpio_motor_L1     = 24
gpio_motor_L2     = 23
gpio_motor_limit_switch = 21
GPIO.setup(gpio_motor_Enable,GPIO.OUT)
GPIO.setup(gpio_motor_L1,GPIO.OUT)
GPIO.setup(gpio_motor_L2,GPIO.OUT)
GPIO.setup(gpio_motor_limit_switch,GPIO.IN)
# Set Motor = OFF
GPIO.output(gpio_motor_Enable,GPIO.LOW)
GPIO.output(gpio_motor_L1,GPIO.LOW) 
GPIO.output(gpio_motor_L2,GPIO.LOW)

                         
def motor_control(type):  
   if MOTOR_OFF == type:
       # Set Enable first
       GPIO.output(gpio_motor_Enable,type[0])       
   # Do L1 and L2                    
   GPIO.output(gpio_motor_L1,type[1]) 
   GPIO.output(gpio_motor_L2,type[2])   
   # Do Enable 
   GPIO.output(gpio_motor_Enable,type[0])
   # Update motor state
   motor_state = type
  

# Read_Motor_Limit_Switch
def motor_limit():
    return GPIO.input(gpio_motor_limit_switch)


# Wait for Motor Limit Switch
def motor_limit_wait(w,p):
   status = 0
   for t in range(0,w):
        time.sleep(.01)
        if 0 == motor_limit():
           #Limit switch event
           if 0 != p:
               time.sleep(p)  
           status = 1
           break;
           
   # Motor stop                   
   motor_control(MOTOR_OFF)
   return status

# Find_Zero
def Find_Zero():    
     motor_control(MOTOR_CW)
     time.sleep(5)
     if motor_limit_wait(10000,.180):    
        time.sleep(1)
        return 1
       
# Rotates Monitor
# Checks rotate sequence
# 1 If motor does not need to be rotate , does not start motor , returns ok
# 2 Starts rotating motor
# 3 Waits 1 second before checking limit switch
# 4 Checks limit switch @ 100 hz , if limit , turns motor off , returns ok
# 5 If limit does not occur in 16 seconds , stops motor , returns error

def rotate(next_motor_position):

    global current_motor_position

    print"Current Motor Position: %s , Next Motor Position %s\n" %(current_motor_position,next_motor_position)

    # Check if rotate is necessary
    if current_motor_position == next_motor_position:
        return current_motor_position

    
    # Check next rotate type 
    if (current_motor_position,next_motor_position) not in MOTOR_ROTATE_SEQ:      
      return 'ROTATE_ERROR'
   
    # Get motor control type needed , start motor
    motor_control(MOTOR_ROTATE_SEQ[(current_motor_position,next_motor_position)])
                  
    # Set return status for failure
    position = 'ROTATE_ERROR'
                  
    # Delay looking at limit switch             
    time.sleep(2)
    
    # Turn off motor when limit switch occurs ..
    # Maximum time for rotation to occur is (5 + (.01 X 1500)) seconds
    p = 0
    if 'CW_90' == next_motor_position:
       p = .150
    if motor_limit_wait(1500,p):
       position = next_motor_position      
      
    
    # Save current motor position
    current_motor_position = position

    
    
    return current_motor_position



   

if __name__ == '__main__':
    print"Motor initalize , ALL = OFF = 0 \n"
    time.sleep(10)
    print"Motor Off \n"
    motor_control(MOTOR_OFF)
    time.sleep(10)
    print "Motor Brake ALL = ON = 1\n"
    motor_control(MOTOR_TEST)     
    time.sleep(10)
    #print"Motor On CW \n"
    #motor_control(MOTOR_CW)
    #time.sleep(10)
    #print"Motor Off \n"
    #motor_control(MOTOR_OFF)
    #time.sleep(1)    
    #motor_control(MOTOR_CCW)
    #print"Motor On CCW \n"
    #time.sleep(10)
    #print"Motor Off \n"
    #motor_control(MOTOR_OFF)
    #Find_Zero()
    #exit()

    
    print"Motor Position CW 90\n"
    rotate('CW_90')
    time.sleep(10)
    
    print"Motor Position ZERO\n"
    rotate('ZERO')
    time.sleep(10)
    
    print"Motor Position ZERO\n"
    rotate('ZERO')
    time.sleep(10)
    """
    """
    print"Motor Position CW 90\n"
    rotate('CW_90')
    time.sleep(10)
    
    
    print"Motor Position CW 90\n"
    rotate('CW_90')
    time.sleep(10)

    print"Motor Position ZERO\n"
    rotate('ZERO')
    time.sleep(10)
    
    
    #Find_Zero()
    
    exit()
    
