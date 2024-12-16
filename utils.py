import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from tkPDFViewer import tkPDFViewer as pdf
import datetime
import sys
import time
import subprocess

# Function to handle the Back button action
def back_to_front():
    subprocess.Popen(["python", "front.py"])  # This will run the front.py script
    # sys.exit()  # Exit the current script
    root.quit()

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

# Path to the folder containing PDFs and the icon
pdf_folder = "Annotation PDF"
icon_path = "icon.png"

# Create the main window
root = tk.Tk()
root.title("PDF File Explorer")
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

# Teacher's Assistant Title
heading_label = tk.Label(heading_frame, text="Annotated PDF's List", fg="white", bg="#666666",
                         font=('TimesNewRoman', 25, 'bold'))
heading_label.pack(fill=tk.X, pady=10)

# State management
is_viewing_pdf = False  # Track whether a PDF is being viewed

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

# Function to update the listbox with PDF files and their icons
def update_pdf_list():
    global is_viewing_pdf
    is_viewing_pdf = False  # Set to False when viewing the list
    for widget in file_frame.winfo_children():
        widget.destroy()  # Clear the frame

    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        file_label = tk.Label(file_frame, text=pdf_file, image=icon_tk, compound=tk.TOP, font=("Arial", 18),fg="#999999", bg="#eaeaea")
        file_label.pack(side=tk.LEFT, padx=5, pady=5)  # Pack horizontally
        file_label.bind("<Button-1>", lambda event, file=pdf_file: open_pdf(file))

    file_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))  # Update scroll region

# Function to handle opening PDF file in the integrated PDF viewer
def open_pdf(file_name):
    global is_viewing_pdf
    is_viewing_pdf = True  # Set to True when viewing a PDF
    pdf_path = os.path.join(pdf_folder, file_name)
    
    # Clear the file_frame and show the PDF viewer
    for widget in file_frame.winfo_children():
        widget.destroy()

    # Create and pack the PDF viewer
    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(file_frame, pdf_location=open(pdf_path, "r"), width=200, height=1000)
    v2.pack(pady=(0, 0))

    file_frame.update_idletasks()

# Function to handle the Esc key behavior
def handle_esc(event):
    global is_viewing_pdf
    if is_viewing_pdf:
        # If viewing a PDF, go back to the home page
        update_pdf_list()
    else:
        # If on the home page, exit the program
        root.quit()

# Bind the Esc key to handle navigation and exit
root.bind("<Escape>", handle_esc)

# Update the listbox with available PDF files
update_pdf_list()

# Create a Back button
back_button = tk.Button(root, text="Back", command=back_to_front, bg="#666666", fg="white", font=('Helvetica', 16))
back_button.pack(side=tk.BOTTOM, pady=200)  # Position the button at the bottom

# Create a menu bar with a refresh button
menubar = tk.Menu(root)
root.config(menu=menubar)
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Refresh", command=update_pdf_list)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

# Run the Tkinter event loop
root.mainloop()
