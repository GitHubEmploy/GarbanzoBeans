import serial
import time
import requests
import threading

ser = serial.Serial("/dev/ttyACMO", 9600)  # Establishing a serial connection with a device on "/dev/ttyACMO" port at a baud rate of 9600
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
    url = "https://plantokyo.up.railway.app/input/3645/" + str(data)  # Creating a URL string with the 'data' variable appended to it
    requests.get(url)  # Sending a GET request to the specified URL
    
threading.Thread(target=main).start()  # Starting a new thread to continuously send requests with the updated 'data' variable
