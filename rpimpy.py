import serial
import time
import requests
import threading
import RPi.GPIO as GPIO

ser = serial.Serial("/dev/ttyACM0", 9600)  # Establishing a serial connection with a device on "/dev/ttyACM0" port at a baud rate of 9600

GPIO.setmode(GPIO.BCM)  # Set GPIO pin numbering mode to BCM

output_pins = [4, 5, 2, 3]  # GPIO pins to send data on

for pin in output_pins:
    GPIO.setup(pin, GPIO.OUT)  # Set the specified GPIO pins as outputs

global data
data = 0  # Initializing a global variable 'data' to 0

def dataupdate():
    global data
    while True:
        data = str(ser.readline())[2:][:-5]  # Reading data from the serial port and storing it in the 'data' variable as a string
        print(data)  # Printing the received data
    
threading.Thread(target=dataupdate).start()  # Starting a new thread to continuously update the 'data' variable

def main():
    global data
    while True:
        # Sending data on GPIO pins
        for i, pin in enumerate(output_pins):
            state = int(data[i])  # Get the state (0 or 1) from the 'data' string
            GPIO.output(pin, state)  # Set the GPIO pin state accordingly
            
        url = "https://plantokyo.up.railway.app/input/3645/" + str(data)  # Creating a URL string with the 'data' variable appended to it
        requests.get(url)  # Sending a GET request to the specified URL

threading.Thread(target=main).start()  # Starting a new thread to continuously send requests with the updated 'data' variable
