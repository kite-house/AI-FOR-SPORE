import time
import keyboard
import threading
import win10toast
import AI
import json

win10toast.ToastNotifier().show_toast("AI FOR SPORE", "Starting program. Please wait 15 second")

time.sleep(15)

with open('config.json', 'r') as config:
    config = json.load(config)

def exit():
    while True:
        time.sleep(0.5)
        if keyboard.is_pressed('q'):
            quit()
    

def go(): 
    AI.load(exit, config["mode"])

exit = threading.Thread(target = exit)
go = threading.Thread(target = go)
if __name__ == '__main__':
    exit.start()
    go.start()