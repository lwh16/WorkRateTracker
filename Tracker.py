from pynput import mouse
from pynput import keyboard
import time
import threading
import math
import sys
from bluetooth import *

#connect to the bluetooth devices
if sys.version < '3':
    input = raw_input

addr = "B8:27:EB:B0:03:7F"

if len(sys.argv) < 2:
    print("no device specified. Searching all nearby bluetooth devices for")
    print("the SampleServer Service")

else:
    addr = sys.argv[1]
    print("Searching for SampleServer on %s" %addr)

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
service_matches = find_service( uuid=uuid, address = addr)

if len(service_matches) == 0:
    print("couldn't find the SampleServer service :(")
    sys.exit(0)

first_match = service_matches[0]
port = first_match["port"]
name = first_match["name"]
host = first_match["host"]

print("connecting to \"%s\" on %s" % (name, host))

#Create the client socket
sock = BluetoothSocet( RFCOMM )
sock.connect((host, port))

print("Connected!")
print("Data being sent...")


def send_details(mouse_travel, key_count, scroll_travel, sock):
    data = mouse_travel + ',' + key_count + ',' + scroll_travel
    sock.send(data)


#functions for capturing the mouse movement etc
def on_move(x, y):
    mouse_log(x,y)

def on_click(x, y, button, pressed):
    #mouse clicks count as keys!
    key_log()

def on_scroll(x, y, dx, dy):
    scroll_log()


def on_release(key):
    key_log()

def key_log():
    key_count[0] += 1

def scroll_log():
    scroll_travel[0] += 0.04 #cm


def mouse_log(x,y):
    #records the position
    global x0
    global y0
    #mouse_times.append([x,y,N])
    mouse_travel[0] += (math.sqrt((x0-x)**2 + (y0-y)**2))/5567 #this will give mouse movement in metres
    x0 = x
    y0 = y

def Mouse_and_keyboard():
    print("Mouse_and_keyboard")
    #join both mouse and keyboard trackers
    with keyboard.Listener(on_release=on_release) as k_listener, mouse.Listener(on_click=on_click, on_scroll=on_scroll,on_move=on_move) as m_listener:
        k_listener.join()
        #m_listener.join()

def keys_per_time():
    #file1.write("mouse travel, key count, scroll travel\n")

    global key_count
    global x0
    global y0
    global mouse_travel
    global scroll_travel

    x0 = 0
    y0 = 0
    key_count = [0]
    mouse_travel = [0]
    scroll_travel = [0]

    timer = time.time()
    print("keys_per_time")
    while True:
        if (time.time() > timer + 30):
            print("---------------------------------")
            #file1 = open("Work_Tracking_9_11_20.txt","a") 
            #file1.write(str(time.time())+ "," + str(mouse_travel[0]) + "," + str(key_count[0]) + "," + str(scroll_travel[0]) + "\n")
            #file1.close()
            send_details(str(mouse_travel[0]), str(key_count[0]), str(scroll_travel[0]), sock)
            timer = time.time()
            key_count = [0]
            mouse_travel = [0]
            scroll_travel = [0]


def mouse_distance(mouse_times):
    #first sort into scrolling and moving
    print("a")


def main():
    #Mouse_and_keyboard()
    #file1 = open("Work_Tracking_9_11_20.txt","a") 
    #file1.truncate(0)
    #file1.write("mouse travel,key count,scroll travel\n")
    #file1.close()
    #print("writing")
    print("MK thread")
    t1 = threading.Thread(target = Mouse_and_keyboard)
    print("time thread")
    t2 = threading.Thread(target = keys_per_time)
  
    # starting thread 1 
    print("MK start")
    t1.start() 

    print("time start")
    # starting thread 2 
    t2.start() 

main()



