import tkinter as tk
import requests
import threading
from PIL import Image, ImageTk
import webbrowser
import random

global data, boxcolor
data = []
boxcolor = 'green'

def dataupdate():
    global data, boxcolor
    while True:
        try:
            data = int(requests.get('https://plantokyo.up.railway.app/data').text)
            #  print(data)
            if int(data) < 12 or int(data) > 50:
                boxcolor = 'red'
            else:
                boxcolor = 'green'
        except:
            print('errored')

def update_button_color(button, color):
    button.configure(bg=color)

def open_dashboard():
    url = 'https://example.com/dashboard'  # Replace with the actual URL of the dashboard
    webbrowser.open(url)

def open_main_page():
    master.deiconify()
    new_window.destroy()

master = tk.Tk()

# Get the screen width and height
screen_width = int(2360/3)
screen_height = int(1640/3)

# Load and resize the background image
background_image = Image.open("Background.png")
background_image = background_image.resize((screen_width, screen_height), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

# Create a canvas widget to hold the buttons and the background image
canvas = tk.Canvas(master, width=screen_width, height=screen_height)
canvas.pack()

# Add the background image to the canvas
canvas.create_image(0, 0, anchor="nw", image=background_photo)

# Load and resize the button images
button_image1 = Image.open("button.png")
button_image1 = button_image1.resize((60, 60), Image.ANTIALIAS)
button_photo1 = ImageTk.PhotoImage(button_image1)

button_image2 = Image.open("button.png")
button_image2 = button_image2.resize((60, 60), Image.ANTIALIAS)
button_photo2 = ImageTk.PhotoImage(button_image2)

button_image3 = Image.open("button.png")
button_image3 = button_image3.resize((60, 60), Image.ANTIALIAS)
button_photo3 = ImageTk.PhotoImage(button_image3)

# Add image buttons at coordinates (50, 50), (150, 150), and (250, 250)
button1 = tk.Button(canvas, image=button_photo1, width=int(1137/21), height=int(1636/21), bg='green')
button1_window = canvas.create_window(120, 270, anchor="nw", window=button1)

button2 = tk.Button(canvas, image=button_photo2, width=int(1137/21), height=int(1636/21), bg=boxcolor, command=open_dashboard)
button2_window = canvas.create_window(370, 250, anchor="nw", window=button2)

button3 = tk.Button(canvas, image=button_photo3, width=int(1137/21), height=int(1636/21), bg='green')
button3_window = canvas.create_window(500, 350, anchor="nw", window=button3)

# Start the data update thread
threading.Thread(target=dataupdate).start()

# Start the button color update thread
def update_button_colors():
    while True:
        button2_color = 'red' if boxcolor == 'red' else 'green'
        update_button_color(button2, button2_color)
        master.update()

threading.Thread(target=update_button_colors).start()

master.attributes('-fullscreen', True)

# Create a new window for the dashboard
new_window = None

def exit_dashboard():
    global new_window
    new_window.destroy()
    master.deiconify()

def show_dashboard():
    global new_window
    master.withdraw()

    new_window = tk.Toplevel(master)
    new_window.attributes('-fullscreen', True)

    # Create the dashboard layout in the new window
    dashboard_frame = tk.Frame(new_window, bg='white')
    dashboard_frame.pack(pady=50)

    # Load and resize the garbage can image
    garbage_can_image = Image.open("button.png")
    garbage_can_image = garbage_can_image.resize((200, 200), Image.ANTIALIAS)
    garbage_can_photo = ImageTk.PhotoImage(garbage_can_image)

    # Add the garbage can image to the dashboard frame
    garbage_can_label = tk.Label(dashboard_frame, image=garbage_can_photo)
    garbage_can_label.grid(row=0, column=0, padx=20, pady=20)

    # Create a StringVar to track the status text
    status_text = tk.StringVar()

    def update_status_text():
        while True:
            # Determine the text based on the button color
            status_text.set("Empty" if boxcolor == 'green' else "Full")
            new_window.update()

    # Start a thread to continuously update the status text
    threading.Thread(target=update_status_text, daemon=True).start()

    # Create the status label and value label
    status_label = tk.Label(dashboard_frame, text="Status:", font=("Arial", 24), bg='white')
    status_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    status_value_label = tk.Label(dashboard_frame, textvariable=status_text, font=("Arial", 24), bg='white')
    status_value_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")

    # Create the trash can status square
    trash_can_status = tk.Canvas(dashboard_frame, width=50, height=50, bg=boxcolor)
    trash_can_status.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    # Create the raw data label and value label
    raw_data_label = tk.Label(dashboard_frame, text="Raw Data:   "+str(data)+"cm", font=("Arial", 24), bg='white')
    raw_data_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    raw_data_value_label = tk.Label(dashboard_frame, textvariable=data, font=("Arial", 24), bg='white')
    raw_data_value_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    # Create the connection strength label and value label
    connection_strength_label = tk.Label(dashboard_frame, text="Connection Strength:", font=("Arial", 24), bg='white')
    connection_strength_label.grid(row=3, column=1, padx=10, pady=10, sticky="w")

    connection_strength_value = random.randint(70, 98)  # Random value for demonstration
    connection_strength_value_label = tk.Label(dashboard_frame, text=connection_strength_value, font=("Arial", 24), bg='white')
    connection_strength_value_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")

    # Create the efficiency label and value label
    efficiency_label = tk.Label(dashboard_frame, text="Efficiency:", font=("Arial", 24), bg='white')
    efficiency_label.grid(row=4, column=1, padx=10, pady=10, sticky="w")
    efficiency_value = random.randint(80, 95)  # Random value for demonstration
    efficiency_value_label = tk.Label(dashboard_frame, text=efficiency_value, font=("Arial", 24), bg='white')
    efficiency_value_label.grid(row=4, column=2, padx=0, pady=10, sticky="w")

    # Update the trash can status square color based on boxcolor
    def update_trash_can_status():
        while True:
            trash_can_status.configure(bg=boxcolor)
            new_window.update()
    
    # Start a thread to continuously update the trash can status square
    threading.Thread(target=update_trash_can_status, daemon=True).start()
    
    # Create a back button to return to the main page
    back_button = tk.Button(new_window, text="Back", command=exit_dashboard, font=("Arial", 16))
    back_button.pack(pady=20)
    
    new_window.mainloop()


# Configure the command of button2 to open the dashboard
button2.configure(command=show_dashboard)

master.mainloop()

