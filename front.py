import tkinter as tk
from tkinter import ttk
import subprocess
import datetime
import time
import sys

# Function to scroll text from right to left
def scroll_text():
    current_text = scrolling_label.cget("text")  # Get the current text
    current_text = current_text[1:] + current_text[0]  # Rotate the text
    scrolling_label.config(text=current_text)  # Update the text in the label
    scrolling_label.after(150, scroll_text)  # Adjust the speed by changing the delay (in milliseconds)

def tick():
    time_string = time.strftime('%H:%M:%S')
    clock.config(text=time_string)
    clock.after(200, tick)

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

# Function to open the whiteboard
def open_whiteboard():
    subprocess.Popen(["python", "wb.py"])  # This will run your wb.py script

# Function to open the presentation control
def open_presentation_control():
    subprocess.Popen(["python", "ppt.py"])  # This will run your ppt.py script

# Function to open the Annotated PDF utility
def open_annotated_pdf():
    subprocess.Popen(["python", "utils.py"])  # This will run your utils.py script

# Function to open the Self Attendance Portal
def open_self_attendance():
    subprocess.Popen(["python", "attendance/main.py"])  # This will run the main.py script from attendance folder

# Function to open the PDF to PPT converter
def open_tools():
    subprocess.Popen(["python", "tools.py"])  # This will run your pdftoppt.py script

# Function to close the application
def close_app(event):
    root.quit()

# Function to exit the application and terminate all Python programs
def exit_program():
    root.quit()
    # sys.exit()  # Terminate the Python program

# Create a full-screen window
root = tk.Tk()
root.title("Teacher's Dashboard")
root.attributes('-fullscreen', True)

# Function to create a gradient background
def create_gradient(canvas, color1, color2):
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    
    r1, g1, b1 = root.winfo_rgb(color1)
    r2, g2, b2 = root.winfo_rgb(color2)
    
    r_ratio = (r2 - r1) / height
    g_ratio = (g2 - g1) / height
    b_ratio = (b2 - b1) / height
    
    for i in range(height):
        nr = int(r1 + (r_ratio * i))
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        
        color = f'#{nr//256:02x}{ng//256:02x}{nb//256:02x}'
        canvas.create_line(0, i, width, i, fill=color)

# Create a canvas for the gradient background
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack(fill="both", expand=True)

# Create the gradient background
create_gradient(canvas, "#eaeaea", "#eaeaea")  # Light gray gradient

# Teacher's Assistant Title
message3 = tk.Label(root, text="Welcome to The Teacher's Assistant", fg="white", bg="#666666", width=55, height=1, font=('Helvetica', 29, 'bold'))
message3.place(relx=0.5, rely=0.2, anchor="center")

# Add a label for the scrolling text
scrolling_label = tk.Label(root, text="Teaching means Teacher's Assistant :)                      ", font=("Helvetica", 26), bg="#eaeaea", fg="#666666")
scrolling_label.place(relx=0.5, rely=0.9, anchor="center")

# Start the scrolling text effect
scroll_text()

# Add a footer
footer = tk.Label(root, text="© 2025 Teacher's Assistant", font=("Helvetica", 14), bg="#2a5298", fg="white")
footer.place(relx=0.5, rely=0.95, anchor="center")  # Positioned near the bottom center

# Custom button style with uniform size and black text
style = ttk.Style()
style.configure("TButton",
                font=("Helvetica", 16),
                padding=10,
                width=25,
                height=2,
                background="#2a5298",
                foreground="black")
style.map("TButton",
          background=[("active", "#1e3c72"), ("!active", "#2a5298")],
          foreground=[("active", "black"), ("!active", "black")])

# Add the Self Attendance Portal button
button_attendance = ttk.Button(root, text="Self Attendance Portal", style="TButton", command=open_self_attendance)
button_attendance.place(relx=0.5, rely=0.3, anchor="center")

# Add the White Board button
button_whiteboard = ttk.Button(root, text="Launch Whiteboard", style="TButton", command=open_whiteboard)
button_whiteboard.place(relx=0.5, rely=0.4, anchor="center")

# Add the Presentation Control button
button_presentation = ttk.Button(root, text="Launch Presentation Control", style="TButton", command=open_presentation_control)
button_presentation.place(relx=0.5, rely=0.5, anchor="center")

# Add the Annotated PDF button
button_annotated_pdf = ttk.Button(root, text="Annotated PDF", style="TButton", command=open_annotated_pdf)
button_annotated_pdf.place(relx=0.5, rely=0.6, anchor="center")

# Add the PDF to PPT Converter button
button_pdf_to_ppt = ttk.Button(root, text="Tools", style="TButton", command=open_tools)
button_pdf_to_ppt.place(relx=0.5, rely=0.7, anchor="center")

# Add the Exit button
button_exit = ttk.Button(root, text="Exit", style="TButton", command=exit_program)
button_exit.place(relx=0.5, rely=0.8, anchor="center")

# Date and Time Display Frames
frame3 = tk.Frame(root, bg="#666666")  # Changed frame color to a blue-gray
frame3.place(relx=0.9, relwidth=0.1, relheight=0.05)  # Increased size for better visibility

frame4 = tk.Frame(root, bg="#666666")  # Changed frame color to a darker blue-gray
frame4.place(relx=0.7, relwidth=0.2, relheight=0.05)  # Increased size for better visibility

# Date and Time Labels
datef = tk.Label(frame4, text=day + "-" + mont[month][:3] + "-" + year, fg="white", bg="#666666", width=55, height=1, font=('Helvetica', 18, 'bold'))
datef.pack(fill='both', expand=1)

clock = tk.Label(frame3, fg="white", bg="#666666", width=55, height=1, font=('Helvetica', 18, 'bold'))
clock.pack(fill='both', expand=1)
tick()

# Bind the Escape key to close the app
root.bind("<Escape>", close_app)

# Run the application
root.mainloop()
