import machine
import utime
from network import Zigbee
import uasyncio as asyncio
import _thread

# Configure GPIO pins for serial data input
serial_pins = [9, 3, 4, 6]  # = GPIO2, GPIO3, GPIO4, GPIO5

# Configure Zigbee parameters
pan_id = b'\x12\x34'  # Pan ID
channel = 15  # Channel
node_id = b'\x01\x02'  # Node ID
home_node = b'\x00\x00'  # Home node address

# Create Zigbee mesh networking object
zb = Zigbee(1)  # UART port number
zb.init(pan_id=pan_id, channel=channel, node_id=node_id)

# Store the combined data from all pins
combined_data = {}

# Function to read data from a GPIO pin
def read_data(pin):
    pin_data = []
    while True:
        data = pin.value()
        pin_data.append(data)
        if len(pin_data) > 10:  # Collect 10 data points
            # Process the collected data using complex logic and sensor fusion
            # Combine the data by summing the values
            combined_data[pin] = sum(pin_data)
            pin_data = []  # Reset the pin data list

# Start a new thread for each GPIO pin
for pin_num in serial_pins:
    pin = machine.Pin(pin_num, machine.Pin.IN)
    _thread.start_new_thread(read_data, (pin,))

# Send the combined data to the home node
async def send_data():
    while True:
        await asyncio.sleep(1)  # Send data every 1 second
        if combined_data:
            # Prepare the data to be sent (e.g., convert to bytes)
            data = bytes(str(combined_data), 'utf-8')
            zb.send(home_node, data)
            combined_data.clear()  # Clear the combined data

# Start the event loop to send data asynchronously
loop = asyncio.get_event_loop()
loop.create_task(send_data())
loop.run_forever()
