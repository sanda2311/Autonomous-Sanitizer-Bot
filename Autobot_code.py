#importing necessary packages

import RPi.GPIO as GPIO                         #for the working of GPIO pins of Raspberry Pi 
from picamera.array import PiRGBArray           #for functioning of raspbery pi camera           
from picamera import PiCamera
import cv2                                      #open cv for image processing
import time                                     #for time calculations inside pogram

#######defining the pins for connection the DC motor with Pi

left1 =21
left2 = 7
right1 = 22
right2 = 24

######################################

tf = 0.030                 #a little delay for smooth functioning of the motor driver IC

dist = 10                  


#########################variables for the calculatin the pulse of ultrasonic sensor to measure the distance of the obstacle
pulse_start= 0;
pulse_end = 0;
#####################################

#######################defining pins for the u;trsonic sensor to be connected wiwth Raspberry PI
TRIG1 = 16
ECHO1 = 18
TRIG2 = 13
ECHO2 = 15
TRIG3 = 11
ECHO3 = 12
##################################

####################33servo motor signal pins connection with Pi
servo1 = 3
servo2 = 5
##############################

#################defining a list of the classes that our caffe model can detect but we have used only the "person" category from this list as we only want to detect whether the obstacle
#################in front of ultrasonic sensor is a person or not
 
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat","bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep","sofa", "train", "tvmonitor"]


#####################

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))





####function for image processing task
def cam():
    camera = PiCamera()                             #initialization of camera
    camera.resolution = (640, 480)                  #decresing resolution of the frame to be captured by Pi camera
    rawCapture = PiRGBArray(camera,size=(640, 480))       
    net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt","MobileNetSSD_deploy.caffemodel")               #loading our deep learning pretrained model to detect whether obstacle is perons or not

    time.sleep(0.1)                                         #giving a small delay
    
    camera.capture(rawCapture, format="bgr")                           #capture an image with camera
    image = rawCapture.array                                           #store the matrix of image captured into image variable

    (h, w) = image.shape[:2]                                            #storing height and width of image in h and w variable
    
    
    
    ####Creates 4-dimensional blob from image. Optionally resizes and crops image from center, subtract mean values, scales values by scalefactor, swap Blue and Red channels.
    
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)             #prerocessing the image captured
    ############################
    
    net.setInput(blob)                       #providing blob to model for predition
    detections = net.forward()              #fedding net to the layer of CNN for predting what class does the image belong to 
    
    human = False                            # initially setting human to False
    for i in np.arange(0, detections.shape[2]):                
        confidence = detections[0, 0, i, 2]           #getting confidence from the output of model like if the image belong to a human then confidence is the percentage that how much percent it belings to that person category

        if confidence > 0.30:                          #if confidence is greater than 30 percent than we become sure that the image captured contains a person 
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            label = CLASSES[idx]                           
            
            #next few lines are commented and it only places a rectangle around the object detected. Was ust used for testing purpose
            if label =="person":
                #cv2.rectangle(image, (startX, startY), (endX, endY),COLORS[idx], 2)
                #y = startY - 15 if startY - 15 > 15 else startY + 15
                #cv2.putText(image, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
                human = True                                   #seting human variable to True if model predicts that image has a person in it 
            
    print(human)
    camera.close()                        #after capturing and processing close the camera
    #cv2.imshow("Output", image)
    #cv2.destroyAllWindows()

    return human

##########defining function for stopping the movement of bot
def stop():
    GPIO.output(left1,False)
    GPIO.output(left2,False)
    GPIO.output(right1,False)
    GPIO.output(right2,False)
    time.sleep(tf)

####################definnig the function for forward movement of bot
def forward():
    GPIO.output(left1,False)
    GPIO.output(left2,True)
    GPIO.output(right1,True)
    GPIO.output(right2,False)
    time.sleep(tf)


####################definnig the function for backward movement of bot
def backward():
    GPIO.output(left1,True)
    GPIO.output(left2,False)
    GPIO.output(right1,False)
    GPIO.output(right2,True)
    time.sleep(tf)



####################definnig the function for right movement of bot
def right():
    GPIO.output(left1,True)
    GPIO.output(left2,False)
    GPIO.output(right1,True)
    GPIO.output(right2,False)
    time.sleep(tf)



####################definnig the function for left movement of bot
def left():
    GPIO.output(left1,False)
    GPIO.output(left2,True)
    GPIO.output(right1,False)
    GPIO.output(right2,True)
    time.sleep(tf)


#we have used three ultrasonic sensors

####checking the distance of obstacle by the leftmost sensor
def check_left_dist():
    GPIO.output(TRIG1, True)
    time.sleep(0.00001)
    GPIO.output(TRIG1, False)

    while GPIO.input(ECHO1)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO1)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    left_dist = pulse_duration * 17150
    left_dist = round(left_dist+1.15,2)
    return left_dist

####checking the distance of obstacle by the rightmost sensor
def check_right_dist():
    GPIO.output(TRIG3, True)
    time.sleep(0.00001)
    GPIO.output(TRIG3, False)

    while GPIO.input(ECHO3)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO3)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    right_dist = pulse_duration * 17150
    right_dist = round(right_dist+1.15,2) 
    return right_dist



####checking the distance of obstacle by the middle/front sensor
def check_front_dist():
    GPIO.output(TRIG2, True)
    time.sleep(0.00001)
    GPIO.output(TRIG2, False)

    while GPIO.input(ECHO2)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO2)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    front_dist = pulse_duration * 17150
    front_dist = round(front_dist+1.15,2) 
    return front_dist



##########main logic for the bot for carrying out the complete procesing

def main():

    GPIO.setmode(GPIO.BOARD)              #setting the pin numbering method of raspberry pi 
    
    
    ####################setting pins as output or input for the sensor and motors
    ###################motors, servo, and trigger pins os ultrasonic sensor will be set as output 
    ##################echo pin will be set as input
    
    GPIO.setup(TRIG1,GPIO.OUT)
    GPIO.setup(ECHO1,GPIO.IN)
    GPIO.setup(TRIG2,GPIO.OUT)
    GPIO.setup(ECHO2,GPIO.IN)
    GPIO.setup(TRIG3,GPIO.OUT)
    GPIO.setup(ECHO3,GPIO.IN)
    GPIO.setup(servo1, GPIO.OUT)
    GPIO.setup(servo2, GPIO.OUT)
    GPIO.setup(left1,GPIO.OUT)
    GPIO.setup(left2,GPIO.OUT)
    GPIO.setup(right1,GPIO.OUT)
    GPIO.setup(right2,GPIO.OUT)
    ###################################
    
    #######initially setting the pins in OFF condition
    GPIO.output(TRIG1, False)
    GPIO.output(TRIG2, False)
    GPIO.output(TRIG3, False)
    #########################
    
    ####for initialization of the servo motor .....a servo motor will work with a PWM signal of 50HZ frequency
    pwm1 = GPIO.PWM(servo1, 50)
    pwm2 = GPIO.PWM(servo2, 50)
    ######################################

    #########setting a threshold distance value for the sensors that is if the distance between obstacle and ultrasonic sensor is less than threshod value than all the process of image processing will be executed
    max_front_dist = 25
    max_left_dist = 20
    max_right_dist = 20
    ##################3
    
    #######starting servo motor with a PWM value of 5 the full rotation of servo motor will be between 0-12 where 0 correspinds to 0 degree and 12 correspinds to 180 degree rotation
    pwm1.start(5)
    pwm2.start(5)
    
    time.sleep(2)              ####giving a little delay for everything to setup
    
    
    ######this will keep on running on and on in loop
    try:
        while True:          
            
            #####string distance calculated by sensors in variables
            front_dist=check_front_dist()
            left_dist=check_left_dist()
            right_dist=check_right_dist()
            ################3
            
            #####logic for the autonomous movement
            
            
            ####if front sendor encounters some obstacle
            if front_dist < max_front_dist:
                stop()
                pwm1.ChangeDutyCycle(7)             #change the angle of servo with camera to face towards the obstacle 
                time.sleep(1)
                isHuman = cam()                     #isHuamn will store the value True of False i.e. whether the obstacle is person or not

                if isHuman==True:                    #if obstacle is person then rotate to shield towards human in order to protect him/her fro the UV light
                    print("human detected")
                    pwm2.ChangeDutyCycle(7)
                    time.sleep(1)
                else:
                    print("human not detected")     

####for autonomous movement....that is after encountering an obstacel turn the not to a side where the obstacle is farther means if the distance from left sensor 20cm and form right sendor it si 30 cm then the  bot will move to the right and vice versa 
                if right_dist > left_dist:
                    if right_dist < max_right_dist and left_dist <max_left_dist:                   #if both senors encounter obstacle that is less then threshold value of distance then bot first move backwards and the figure out left or right
                        stop()
                        time.sleep(tf)
                        backward()
                        time.sleep(1)
                    else:
                        right()
                        time.sleep(0.5)
                elif left_dist > right_dist:
                    if right_dist < max_right_dist and left_dist <max_left_dist:
                        stop()
                        time.sleep(tf)
                        backward()
                        time.sleep(1)
                    else:
                        left()
                        time.sleep(0.5)

###############if obstacle is on right then take snapshot process it and check whether human or not and move the shield the accordingly and then rotate to the left
            elif right_dist < max_right_dist:
                stop()
                pwm1.ChangeDutyCycle(11)
                time.sleep(1)
                isHuman = cam()

                if isHuman==True:
                    print("human detected")
                    pwm2.ChangeDutyCycle(11)
                    time.sleep(1)
                else:
                    print("human not detected")
                left()
                time.sleep(0.5)
                
############same as uppper one but rotate to rigth
            elif left_dist < max_left_dist:
                stop()
                pwm1.ChangeDutyCycle(3)
                time.sleep(1)
                isHuman = cam()

                if isHuman==True:
                    print("human detected")
                    pwm2.ChangeDutyCycle(3)
                    time.sleep(1)
                else:
                    print("human not detected")
                right()
                time.sleep(0.5)


#####if there is not obstacle then keep on moving forward
            else:
                forward()
        
#######if CTRl+C is pressed the program will terminate and all the pins of raspberry pi will be cleared whichever logic they hold right now
    except KeyboardInterrupt:
        GPIO.cleanup()
        


####for calling the main function
if __name__ == '__main__':
    main()