
import time
from pynput import keyboard
from threading import Thread

canRun = True
stateUp = False
stateRight = False
stateLeft = False
stateDown = False
stateShift = False

def doit():
	while canRun:
		print("UP - %s, RIGHT - %s, DOWN - %s, LEFT = %s, Shift - %s" %
			(stateUp, stateRight, stateDown, stateLeft, stateShift))
		time.sleep(0.5) #500ms

my_thread = Thread(target = doit)
my_thread.start()
def on_move(key, isPressed):
	global stateUp, stateRight, stateLeft, stateDown, stateShift
	if key == keyboard.Key.up:
	    stateUp = isPressed
	if key == keyboard.Key.right:
		stateRight = isPressed
	if key == keyboard.Key.down:
		stateDown = isPressed
	if key == keyboard.Key.left:
		stateLeft = isPressed
	if key == keyboard.Key.shift:
		stateShift = isPressed

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
