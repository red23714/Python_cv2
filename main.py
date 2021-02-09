import time
import serial
import time
import struct

from pynput import keyboard
from threading import Thread

arduino = serial.Serial('COM16', 115200, timeout=.1)

canRun = True
stateUp = False
stateRight = False
stateLeft = False
stateDown = False
stateShift = False

def doit():
	while canRun:
		print(stateUp, stateRight, stateDown, stateLeft, stateShift)
		time.sleep(2) #500ms

my_thread = Thread(target = doit)
my_thread.start()
def on_move(key, isPressed):
	global stateUp, stateRight, stateLeft, stateDown, stateShift


	if key == keyboard.Key.up:
		arduino.write(b'2')
		stateUp = isPressed
		if(stateUp == False):
			arduino.write(b'0')
	if key == keyboard.Key.right:
		arduino.write(b'3')
		stateRight = isPressed
		if (stateRight == False):
			arduino.write(b'0')
	if key == keyboard.Key.down:
		arduino.write(b'4')
		stateDown = isPressed
		if (stateDown == False):
			arduino.write(b'0')
	if key == keyboard.Key.left:
		arduino.write(b'1')
		stateLeft = isPressed
		if (stateLeft == False):
			arduino.write(b'0')

	if key == keyboard.Key.shift:
		stateShift = isPressed

	time.sleep(0.01)

def on_press_custom(key):
	global canRun
	on_move(key, True)
	if hasattr(key, 'char') and key.char == 'q':
		canRun = False
def on_release_custom(key):
	on_move(key, False)

listener = keyboard.Listener(
	on_press=on_press_custom,
	on_release=on_release_custom)
listener.start()
