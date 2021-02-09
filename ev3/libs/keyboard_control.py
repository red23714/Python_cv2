import serial
from pynput import keyboard
from pynput.keyboard import Key, Controller


class KeyDetector:
    protocolSSH = 'SSH'
    protocolSerial = 'Serial'

    def __init__(self, protocol=protocolSSH, serialPort='COM1'):
        # For Windows serialPort = 'COMX'
        # For Mac serialPort = '/dev/cu.usbmodemXXXXX'
        self.protocol = protocol
        self.controls = [False, False, False, False]
        self.controller = Controller()
        self.keyboard = keyboard
        self.arduino = None
        if self.protocol == self.protocolSerial:
            self.arduino = serial.Serial(port=serialPort, baudrate=115200, timeout=.1)

    def command_LEFT(self):
        if self.protocol == self.protocolSSH: self.sendDirectCommand('1')
        if self.protocol == self.protocolSerial: self.arduino.write(b'1')

    def command_UP(self):
        if self.protocol == self.protocolSSH: self.sendDirectCommand('2')
        if self.protocol == self.protocolSerial: self.arduino.write(b'2')

    def command_RIGHT(self):
        if self.protocol == self.protocolSSH: self.sendDirectCommand('3')
        if self.protocol == self.protocolSerial: self.arduino.write(b'3')

    def command_DOWN(self):
        if self.protocol == self.protocolSSH: self.sendDirectCommand('4')
        if self.protocol == self.protocolSerial: self.arduino.write(b'4')

    def command_PAUSE(self):
        if self.protocol == self.protocolSSH: self.sendDirectCommand('0')
        if self.protocol == self.protocolSerial: self.arduino.write(b'0')

    def sendDirectCommand(self, targetKey):
        self.controller.press(targetKey)
        self.controller.release(targetKey)
        self.controller.press(Key.enter)
        self.controller.release(Key.enter)

    def onMove(self, key, isPressed):
        if key == self.keyboard.Key.left or hasattr(key, 'char') and key.char == 'a':
            self.controls[0] = isPressed
        if key == self.keyboard.Key.up or hasattr(key, 'char') and key.char == 'w':
            self.controls[1] = isPressed
        if key == self.keyboard.Key.right or hasattr(key, 'char') and key.char == 'd':
            self.controls[2] = isPressed
        if key == self.keyboard.Key.down or hasattr(key, 'char') and key.char == 's':
            self.controls[3] = isPressed
        return self.controls

    def isExitKey(self, key):
        return key == self.keyboard.Key.esc or hasattr(key, 'char') and key.char == 'q'

    def isMoving(self):
        return self.controls[0] or self.controls[1] or self.controls[2] or self.controls[3]

    def canStop(self):
        return not self.controls[0] and not self.controls[1] and not self.controls[2] and not self.controls[3]


