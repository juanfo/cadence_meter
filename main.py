from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import Qt

import serial
import threading

label = None

# this port address is for the serial tx/rx pins on the GPIO header
SERIAL_PORT = '/dev/cu.usbmodem144101'
# be sure to set this to the same rate used on the Arduino
SERIAL_RATE = 9600


def decode_serial():
    ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
    while True:
        # using ser.readline() assumes each line contains a single reading
        # sent using Serial.println() on the Arduino
        reading = ser.readline().decode('utf-8')
        # reading is a string...do whatever you want from here
        set_cadence(reading.split()[1])


def set_cadence(cadence):
    global label
    if label == None:
        return
    text_color = 'green'
    n_cadence = int(cadence)
    if n_cadence > 85:
        text_color = 'orange'
    if n_cadence > 99:
        text_color = 'red'
    if n_cadence > 200 and n_cadence != 666:
        return
    label.setStyleSheet('QLabel {{ background-color : black; color : {}; text-align: right}}'.format(text_color))
    label.setText(cadence)


x = threading.Thread(target=decode_serial)
x.start()
app = QApplication([])
label = QLabel('')
label.setFont(QtGui.QFont("Helvetica", 600, QtGui.QFont.Bold))
label.setAlignment(Qt.Qt.AlignCenter)
set_cadence('666')
label.show()
app.exec_()
