import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import datetime
import time
import sys
import subprocess  # For opening PowerPoint files

######################################## USED STUFFS ############################################

global key
key = ''

ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day, month, year = date.split("-")

mont = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

##################################################################################

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

# Path to the folder containing PPTs and the icon
ppt_folder = "Created ppt"
icon_path = "icon.png"

# Create the main window
root = tk.Tk()
root.title("PPT File Explorer")
root.configure(bg="#eaeaea")  # Set background color to #eaeaea

# Create a frame for Date and Time
date_time_frame = tk.Frame(root, bg="#999999")
date_time_frame.pack(side=tk.TOP, fill=tk.X)

frame4 = tk.Frame(date_time_frame, bg="#666666")
frame4.pack(side=tk.RIGHT, fill=tk.X, expand=True)

date_label = tk.Label(frame4, text=day + "-" + mont[month][:3] + "-" + year, fg="white", bg="#666666",
                      font=('Helvetica', 14, 'bold'))
date_label.pack(fill='both', expand=1)

frame3 = tk.Frame(date_time_frame, bg="#666666")
frame3.pack(side=tk.RIGHT, fill=tk.X, expand=True)

clock = tk.Label(frame3, fg="white", bg="#666666",
                 font=('Helvetica', 14, 'bold'))
clock.pack(fill='both', expand=1)

tick()  # Start the clock

# Create a frame for the heading
heading_frame = tk.Frame(root, bg="#666666", pady=10)
heading_frame.pack(side=tk.TOP, fill=tk.X)

# Title for Created PPTs
heading_label = tk.Label(heading_frame, text="Created PPTs List", fg="white", bg="#666666",
                         font=('TimesNewRoman', 25, 'bold'))
heading_label.pack(fill=tk.X, pady=10)

# State management
is_viewing_ppt = False  # Track whether a PPT is being viewed

# Set the window icon (optional, can be removed if not needed)
try:
    root.iconphoto(True, ImageTk.PhotoImage(Image.open(icon_path)))  # Set application icon
except Exception as e:
    print(f"Warning: {e}")

# Make the window full screen
root.attributes("-fullscreen", True)
root.bind("<F11>", lambda event: root.attributes("-fullscreen", not root.attributes("-fullscreen")))

# Load the icon image
try:
    icon_image = Image.open(icon_path)
    icon_image = icon_image.resize((120, 120))  # Resize icon to fit the UI
    icon_tk = ImageTk.PhotoImage(icon_image)
except Exception as e:
    print(f"Warning: {e}")
    icon_tk = None

# Create a frame for the listbox
frame = tk.Frame(root, bg="#eaeaea")  # Set background color for the frame
frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas for displaying the list of files with icons
canvas = tk.Canvas(frame, bg="#eaeaea")  # Set background color for the canvas
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Add a horizontal scrollbar to the canvas
h_scroll = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
canvas.config(xscrollcommand=h_scroll.set)

# Create a frame inside the canvas for the list of files
file_frame = tk.Frame(canvas, bg="#eaeaea")  # Set background color for the file list frame
canvas.create_window((0, 0), window=file_frame, anchor=tk.NW)

# Function to update the listbox with PPT files and their icons
def update_ppt_list():
    global is_viewing_ppt
    is_viewing_ppt = False  # Set to False when viewing the list
    for widget in file_frame.winfo_children():
        widget.destroy()  # Clear the frame

    ppt_files = [f for f in os.listdir(ppt_folder) if f.endswith('.pptx')]
    
    for ppt_file in ppt_files:
        file_label = tk.Label(file_frame, text=ppt_file, image=icon_tk, compound=tk.TOP, font=("Arial", 18), fg="#999999", bg="#eaeaea")
        file_label.pack(side=tk.LEFT, padx=5, pady=5)  # Pack horizontally
        file_label.bind("<Button-1>", lambda event, file=ppt_file: open_ppt(file))

    file_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))  # Update scroll region

# Function to handle opening PPT file in the default viewer
def open_ppt(file_name):
    global is_viewing_ppt
    is_viewing_ppt = True  # Set to True when viewing a PPT
    ppt_path = os.path.join(ppt_folder, file_name)

    # Attempt to open the PowerPoint file
    try:
        subprocess.Popen([ppt_path], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open the PPT file: {e}")

    # Update the list to show available PPTs
    update_ppt_list()

# Function to handle the Esc key behavior
def handle_esc(event):
    global is_viewing_ppt
    if is_viewing_ppt:
        # If viewing a PPT, go back to the home page
        update_ppt_list()
    else:
        # If on the home page, exit the program
        root.quit()

# Function to handle the Back button action
def back_to_front():
    subprocess.Popen(["python", "front.py"])  # This will run the front.py script
    sys.exit()  # Exit the current script

# Bind the Esc key to handle navigation and exit
root.bind("<Escape>", handle_esc)

# Update the listbox with available PPT files
update_ppt_list()

# Create a Back button
back_button = tk.Button(root, text="Back", command=back_to_front, bg="#666666", fg="white", font=('Helvetica', 16))
back_button.pack(side=tk.BOTTOM, pady=200)  # Position the button at the bottom

# Create a menu bar with a refresh button
menubar = tk.Menu(root)
root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Refresh", command=update_ppt_list)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Run the Tkinter event loop
root.mainloop()
