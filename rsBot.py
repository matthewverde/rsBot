from pynput.mouse import Button, Controller
from pynput import mouse
import pyscreenshot
import numpy as np
from PIL import Image
import time
import datetime

clickableMouse = Controller()
# Read pointer position
#print('The current pointer position is {0}'.format(
    #mouse.position))

# Set pointer position
#mouse.position = (10, 20)
#print('Now we have moved it to {0}'.format(
    #mouse.position))

# Move pointer relative to current position
#mouse.move(5, -5)

# Press and release
#mouse.press(Button.left)
#mouse.release(Button.left)

# Double click; this is different from pressing and releasing
# twice on Mac OSX
#mouse.click(Button.left, 2)

# Scroll two steps down
#mouse.scroll(0, 2)

def on_move(x, y):
    print('X: {0}, Y: {1}'.format(x, y))

def toWillow():
    clickableMouse.position = (960, 158)
    clickableMouse.click(Button.left, 1)

def toBank():
    clickableMouse.position = (1000, 100)
    clickableMouse.click(Button.left, 1)

#homeBase = 979, 129.5
#move in groups of 2.5
#example, move to the right is 981.5, 129.5

#be looking true north
def moveXY(x, y):
    homeX = 979
    homeY = 129.5
    increment = 4.0
    newX = homeX + (x * increment)
    newY = homeY + (y * increment)
    clickableMouse.position = (newX, newY)
    time.sleep(0.5)
    clickableMouse.click(Button.left, 1)

#zoomed all the way in
#pos is in the following form
#1 2 3
#4 5 6
#7 8 9
#where 5 is the character

#(520,160) () ()
#(520,250) () ()
#(520,340) () ()
def clickPosition(pos, rightClick):
    startPos = (0,0)
    increment = 90
    mult = 0
    startX = 485
    startY = 0
    print(clickableMouse.position)
    if pos < 4:
        startY = 170
        mult = pos - 1
    elif pos < 7:
        startY = 260
        mult = pos - 4
    else:
        startY = 350
        mult = pos - 7
    startPos = (startX + (mult * increment), startY)
    clickableMouse.position = startPos
    time.sleep(0.5)
    if rightClick:
        clickableMouse.click(Button.right, 1)
    else:
        clickableMouse.click(Button.left, 1)

def isInvFull():
    base = getRGB('envSpot/base.png')
    takePhotoOfLastInvSpot()
    cur = getRGB('envSpot/env.png')
    #print('{0}, {1}, {2}'.format(base[0], base[1], base[2]))
    #print('{0}, {1}, {2}'.format(cur[0], cur[1], cur[2]))

    if abs(base[0] - cur[0]) < 1000 and abs(base[1] - cur[1]) < 1000  and abs(base[2] - cur[2]) < 1000:
        return False
    return True

def takePhotoOfLastInvSpot():
    screenshot = pyscreenshot.grab(bbox=(1020, 470, 1060, 510))
    screenshot.save('envSpot/env.png')

def getRGB(pathname):
    r = 0
    b = 0
    g = 0
    img = Image.open(pathname)
    arr = np.array(img)
    lenx = len(arr)
    leny = len(arr[0])
    for x in range(lenx):
        for y in range(leny):
            r += arr[x,y,0]
            g += arr[x,y,1]
            b += arr[x,y,2]
    return (r, g, b)


def chopWillow():
    #go to willow
    moveXY(-5, 6)
    time.sleep(10)
    invFull = False
    #chop willow
    while invFull is not True:
        clickPosition(4, False)
        time.sleep(7)
        invFull = isInvFull()

def clickEmptyEnv():
    clickableMouse.position = (785, 350)
    time.sleep(1)
    clickableMouse.click(Button.left, 1)

def emptyInv():
    moveXY(5, -6)
    time.sleep(10)
    clickPosition(4, False)
    time.sleep(1)
    clickEmptyEnv()
    time.sleep(1)

def formatTime(curSeconds):
    return str(datetime.timedelta(seconds=curSeconds))

#THIS IS THE MAIN FUNCTION OF THE PROGRAM
#call this to run the bot
def runBot():
    initStats()
    while 1:
        chopWillow()
        emptyInv()
        updateStats()

def initStats():
    global totalLoads
    totalLoads = 0
    global totalTime
    totalTime = 0
    global curLoads
    curLoads = 0
    global curTime
    curTime = 0
    global startTime
    startTime = 0
    startTime = time.time()
    global lastTime
    lastTime = time.time()
    statFile = open('stats/botStats.txt', 'r')
    lines = []
    for line in statFile:
        lines.append(line)
    print(lines)
    if len(lines) > 0:
        totalLoads = float(lines[0])
        totalTime = float(lines[1])
    print('loaded time:\t%d' % totalTime)
    print('loaded total loads:\t%d' % totalLoads)
    statFile.close()
    
def updateStats():
    logsPerLoad = 28
    experiencePerLog = 67.5
    global totalLoads
    global totalTime
    global curLoads
    global curTime
    global startTime
    global lastTime
    loadTime = time.time() - lastTime
    lastTime = time.time()
    totalTime += loadTime
    curTime += loadTime
    totalLoads += 1
    curLoads += 1
    statFile = open('stats/botStats.txt', 'w')
    statFile.write('{0}\n{1}'.format(totalLoads, totalTime))
    statFile.close()
    print('***Load Stats***')
    print('Load Stats:')
    print('Current Session Loads:\t{0}'.format(curLoads))
    print('Current Session Logs:\t%d' % (curLoads * logsPerLoad))
    print('Current Session Experience:\t%d' % ((curLoads * logsPerLoad) * experiencePerLog))
    print('Total Loads:\t{0}'.format(totalLoads))
    print('Total Logs:\t%d' % (totalLoads * logsPerLoad))
    print('Total Experience:\t%d' % ((totalLoads * logsPerLoad) * experiencePerLog))
    print('Time:')
    print('Last Load Time:\t{0}'.format(formatTime(loadTime)))
    print('Session Run Time:\t{0}'.format(formatTime(curTime)))
    print('Total Run Time:\t{0}'.format(formatTime(totalTime)))
    print('Session Avg Load Time:\t{0}'.format(formatTime(curTime / curLoads)))
    print('Total Avg Load Time:\t{0}'.format(formatTime(totalTime / totalLoads)))
    print('******************************************\n')


totalLoads = 0
totalTime = 0
curLoads = 0
curTime = 0
startTime = 0
lastTime = 0
runBot()



        



#with mouse.Listener(on_move=on_move) as listener:
    #listener.join()
    