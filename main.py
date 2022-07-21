import RPi.GPIO as GPIO
import time
from time import sleep
import cv2
import json
from tinydb import TinyDB, Query
import requests
from base64 import b64encode
from IPython.display import Image
from matplotlib import rcParams
global steps_count
steps_count = 0
global rotations
rotations = 1
rcParams['figure.figsize'] = 10, 20
img_counter = 1

import drivers
display = drivers.Lcd()
printf = display.lcd_display_string
global retry
retry = 0
numbers = []
db = TinyDB('IC_db.json')
User = Query()
db2 = TinyDB('USER_db.json')
User2 = Query()
DIR = 26   # Direction GPIO Pin
STEP = 7  # Step GPIO Pin
in1 = 22
in2 = 11
sensor = 4
GPIO.setmode(GPIO.BCM)

GPIO.setup(sensor,GPIO.IN)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.output(DIR, 1)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)
buttonstate = GPIO.input(27)
MODE = (14, 15, 23)   # Microstep Resolution GPIO Pins
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (1, 1, 1)}
GPIO.output(MODE, RESOLUTION['1/8'])

steps_count = steps_count * 8
delay = .0154 / 8
L1 = 5
L2 = 6
L3 = 13
L4 = 19

# These are the four columns
C1 = 12
C2 = 16
C3 = 20
C4 = 21

# The GPIO pin of the column of the key that is currently
# being held down or -1 if no key is pressed
keypadPressed = -1


inputted = ""

# Setup GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

# Use the internal pull-down resistors
GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# This callback registers the key that was pressed
# if no other key is currently pressed
GPIO.setwarnings(False)
def search():
    results11 = (db.search(User.PartNumber == output1))
    for x in results11:
     main_output=(x['Description'])
     print(main_output)
    for y in results11:
        stepangle=(y['Angle'])
        print(stepangle)
    if stepangle <= 800:
        step = stepangle
        stepper(step, 1)
    else:
        step = 1600 - stepangle
        stepper(step, 0)


def search1():
    results12 = (db.search(User.PartNumber == output2))
    for x in results12:
     main_output1=(x['Description'])
     print(main_output1)
    for y in results12:
        stepangle=(y['Angle'])
        print(stepangle)
    if stepangle <= 800:
        step = stepangle
        stepper(step, 1)
    else:
        step = 1600 - stepangle
        stepper(step, 0)


def stepper(step_count, rotation):
    global steps_count
    global rotations
    global free
    global retry
    rotations = rotation
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, rotations)
    MODE = (14, 15, 23)  # Microstep Resolution GPIO Pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (1, 1, 1)}
    GPIO.output(MODE, RESOLUTION['1/8'])

    steps_count = step_count
    delay = .0154 / 8
    for x in range(steps_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        

    sleep(2)
    rotations = int(not (rotations))
    print("rotation=",rotations)
    if free == 1:
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        sleep(0.2)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        sleep(0.2)
        retry = 0
    
    
def stepper2(step_count, rotation):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, rotation)
    MODE = (14, 15, 23)  # Microstep Resolution GPIO Pins
    GPIO.setup(MODE, GPIO.OUT)
    RESOLUTION = {'Full': (0, 0, 0),
                  'Half': (1, 0, 0),
                  '1/4': (0, 1, 0),
                  '1/8': (1, 1, 0),
                  '1/16': (1, 1, 1)}
    GPIO.output(MODE, RESOLUTION['1/8'])

    delay = .0154 / 8
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    
    sleep(.5)
    rotation = int(not (rotation))
    GPIO.output(DIR, rotation)
    print(rotation)
    display.lcd_clear()
    printf("Press A to",1)
    printf("continue..",2)
    entering = keypadinput()
    for x in range(step_count):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    sleep(.5)
    
def keypadCallback(channel):
    global keypadPressed
    if keypadPressed == -1:
        keypadPressed = channel

# Detect the rising edges on the column lines of the
# keypad. This way, we can detect if the user presses
# a button when we send a pulse.
GPIO.add_event_detect(C1, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C2, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C3, GPIO.RISING, callback=keypadCallback)
GPIO.add_event_detect(C4, GPIO.RISING, callback=keypadCallback)

# Sets all lines to a specific state. This is a helper
# for detecting when the user releases a button
def setAllLines(state):
    GPIO.output(L1, state)
    GPIO.output(L2, state)
    GPIO.output(L3, state)
    GPIO.output(L4, state)

def checkSpecialKeys():
    global inputted
    global resultant
    pressed = False

    GPIO.output(L1, GPIO.HIGH)

    if (not pressed and GPIO.input(C4) == 1):
        resultant= inputted
        print (resultant)
        pressed = True

    GPIO.output(L3, GPIO.LOW)

    if pressed:
        inputted = ""

    return pressed

# reads the columns and appends the value, that corresponds
# to the button, to a variable
def readLine(line, characters):
    global inputted
    # We have to send a pulse on each line to
    # detect button presses
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        inputted = inputted + characters[0]
    if(GPIO.input(C2) == 1):
        inputted = inputted + characters[1]
    if(GPIO.input(C3) == 1):
        inputted = inputted + characters[2]
    if(GPIO.input(C4) == 1):
        inputted = inputted + characters[3]
    GPIO.output(line, GPIO.LOW)

def keypadinput():
    global keypadPressed
    while True:
        # If a button was previously pressed,
        # check, whether the user has released it yet
        if keypadPressed != -1:
            setAllLines(GPIO.HIGH)
            if GPIO.input(keypadPressed) == 0:
                keypadPressed = -1
            else:
                time.sleep(0.1)
        # Otherwise, just read the input
        else:
            if not checkSpecialKeys():
                readLine(L1, ["1","2","3","A"])
                readLine(L2, ["4","5","6","B"])
                readLine(L3, ["7","8","9","C"])
                readLine(L4, ["*","0","#","D"])
                time.sleep(0.1)
            else:
                global resultant
                time.sleep(0.1)
                break
    return resultant
    resultant = ""

def insert():
    db.insert({'PartNumber': '0', 'Description': 'Trash','Angle': 0, 'Angle2': 800})
    db.insert({'PartNumber': '74192', 'Description': '', 'Angle': 800, 'Angle2': 0})
    db.insert({'PartNumber': '7485', 'Description': 'PrecisionTimer', 'Angle': 1000, 'Angle2': 200})
    db.insert({'PartNumber': '7432', 'Description': 'DualOperationalAmplifier', 'Angle': 1200, 'Angle2': 400})
    db.insert({'PartNumber': '7402', 'Description': '4-BitBinaryFullAdder', 'Angle': 1400, 'Angle2': 600})
    db.insert({'PartNumber': '7420', 'Description': '4-BitComparator', 'Angle': 175, 'Angle2': 1000})

insert()
#db.truncate()
def makeImageData(imgpath):
    img_req = None
    with open(imgpath, 'rb') as f:
        ctxt = b64encode(f.read()).decode()
        img_req = {
            'image': {
                'content': ctxt
            },
            'features': [{
                'type': 'DOCUMENT_TEXT_DETECTION',
                'maxResults': 1
            }]
        }
    return json.dumps({"requests": img_req}).encode()

def requestOCR(url, api_key, imgpath):
    imgdata = makeImageData(imgpath)
    response = requests.post(ENDPOINT_URL,
                             data=imgdata,
                             params={'key': api_key},
                             headers={'Content-Type': 'application/json'})

    return response

while (buttonstate == True):
    global free
    reverse = 0
    free = 0
    printf("SORTING MODE",1)
    sleep(2)
    buttonstate = GPIO.input(27)
    if buttonstate == False:
        break
    if retry == 4:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        sleep(0.1)
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        sleep(0.1)
        retry = 0
    if retry > 0:
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        sleep(0.03)
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        sleep(0.03)
        print("3")
    while (GPIO.input(sensor) == 1):
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        sleep(0.003)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        sleep(0.003)
        retry = 0
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    
    if retry == 0:
        print(steps_count)
        print(rotations)
        stepper(steps_count, rotations)
        steps_count = 0
    display.lcd_clear()
    printf("scanning",1)
    capture = cv2.VideoCapture(0)
    while True:
      sleep(1)
      _, frame = capture.read()
      screenshot = "opencv_frame_{}.png".format(img_counter)
      cv2.imwrite(screenshot,frame)
      image1 = cv2.imread(screenshot)
      print("1")
      capture.release()
      break
    while True:
        if reverse == 1:
            break
        print("2")
        with open('ServiceAccountToken.json') as f:
             data = json.load(f)
             ENDPOINT_URL = 'https://vision.googleapis.com/v1/images:annotate'
             api_key = data["api_key"]
             img_loc = "opencv_frame_{}.png".format(img_counter)
             Image(img_loc)
             img_counter += 1
             result = requestOCR(ENDPOINT_URL, api_key, img_loc)
             if result.status_code != 200 or result.json().get('error'):
                 print("Error")
             else:
                 resultjson = result.json()['responses']
                 print(resultjson)
                 if resultjson == [{}]:
                     retry += 1
                     reverse = 1
                     steps_count = 0
                     break
                 else:
                     result = result.json()['responses'][0]['textAnnotations']
                     

             IC=result[0]["description"]
             nlines=IC.count('\n')
             if nlines>1:
                 outputstring1= IC.split("\n", (nlines-1))[nlines-1]
                 for word in outputstring1:
                     if word.isdigit():
                         numbers.append(word)
                 output1=''.join(numbers)
                 print(output1)
                 results11 = (db.search(User.PartNumber == output1))
                 print(results11)
                 if results11 == []:
                     reverse = 1
                     retry += 1
                     output1 = 0
                     numbers.clear()
                 else:
                     display.lcd_clear()
                     printf(output1,1)
                     reverse = 1
                     free = 1
                     display.lcd_clear()
                     printf(output1,1)
                     sleep(1)
                     search()
                     numbers.clear()
             else:
                 for word in IC:
                     if word.isdigit():
                         numbers.append(word)
                 output2 = ''.join(numbers)
                 print(output2)
                 results12 = (db.search(User.PartNumber == output2))
                 print(results12)
                 if results12 == []:
                     retry += 1
                     reverse = 1
                     output2 = 0
                     numbers.clear()
                 else:
                     display.lcd_clear()
                     printf(output2,1)
                     free = 1
                     reverse = 1
                     display.lcd_clear()
                     printf(output2,1)
                     sleep(1)
                     search1()
                     numbers.clear()

while buttonstate == False:
    GPIO.setwarnings(False)
    mainangle = 0
    mainangle2 = 0
    display.lcd_clear()
    ic = []
    name = ""
    printf("VENDING MODE",1)
    name = input()
    display.lcd_clear()
    printf(name,1)
    sleep(2)
    buttonstate = GPIO.input(27)
    if buttonstate == True:
        break
    results111 = (db2.search(User2.USN == name))
    if results111 == []:
        display.lcd_clear()
        printf("Enter No. of",1)
        printf("Types of IC's",2)
        nic = int(keypadinput())
        for x in range (0, nic):
            display.lcd_clear()
            printf("Enter IC No.",1)
            IC = str(keypadinput())
            printf(IC,2)
            anglesearch = (db.search(User.PartNumber == IC))
            for x in anglesearch:
                mainangle=(x['Angle2'])
            if mainangle <= 800:
                stepic = mainangle
                stepper2(stepic, 1)
            else:
                stepic = 1600-mainangle
                stepper2(stepic, 0)
            ic.append(IC)
        db2.insert({'USN': name, 'NO of types of IC': nic,'IC': ic})
        display.lcd_clear()
        printf("Database saved",1)
    else:
        display.lcd_clear()
        printf(name,2)
        printf("HI...",1)
        numbersearch2 = (db2.search(User2.USN == name))
        for x in numbersearch2:
            mainnumber=(x['NO of types of IC'])
        for y in numbersearch2:
            ICn=(y['IC'])
        for z in range (0, mainnumber):
            display.lcd_clear()
            printf("Return IC:",1)
            printf(ICn[z],2) 
            anglesearch2 = (db.search(User.PartNumber == ICn[z]))
            for x in anglesearch2:
                mainangle2=(x['Angle2'])
            if mainangle2 <= 800:
                stepic2 = mainangle2
                print(stepic2)
                stepper2(stepic2, 1)
            else:
                stepic2 = 1600-mainangle2
                stepper2(stepic2, 0)
        db2.remove(User2.USN == name)
        display.lcd_clear()
