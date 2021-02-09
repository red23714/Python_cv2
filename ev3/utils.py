import time
from libs.keyboard_control import KeyDetector
from threading import Thread
canRun = True
controls = [False, False, False, False] #LEFT, UP, RIGHT, DOWN
isMoving = False
def doit():
	global isMoving
	while canRun:
		print("LEFT - %s, UP - %s, RIGHT - %s, DOWN = %s" %
			(controls[0], controls[1], controls[2], controls[3]))
		if controls[0]: kd.command_LEFT(); isMoving = True
		if controls[1]: kd.command_UP(); isMoving = True
		if controls[2]: kd.command_RIGHT(); isMoving = True
		if controls[3]: kd.command_DOWN(); isMoving = True
		if isMoving:
			if kd.canStop():
				isMoving = False
				kd.command_PAUSE()
		time.sleep(0.025) #25ms
kd = KeyDetector() #For SSH connection only
#kd = KeyDetector(protocol=KeyDetector.protocolSerial, serialPort='COM4')
my_thread = Thread(target = doit)
my_thread.start()
def on_press_custom(key):
	global canRun, controls
	controls = kd.onMove(key, True)
	if kd.isExitKey(key):
		canRun = False
def on_release_custom(key):
	global controls
	controls = kd.onMove(key, False)
listener = kd.keyboard.Listener(
	on_press=on_press_custom,
	on_release=on_release_custom)
listener.start()
