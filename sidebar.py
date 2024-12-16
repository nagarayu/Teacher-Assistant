import os
from tkinter import *
from PIL import Image, ImageTk

# Function to load images from the "Presentation" folder
def load_images():
    images = []
    folder_path = 'Presentation'
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, file_name)
            img = Image.open(img_path)
            img.thumbnail((300, 300))  # Resize image to fit in the sidebar
            images.append(ImageTk.PhotoImage(img))
    return images

# Function to display the images in the sidebar
def display_images():
    images = load_images()
    for idx, img in enumerate(images):
        img_label = Label(frame, image=img, borderwidth=2, relief="groove")
        img_label.image = img  # Keep reference to avoid garbage collection
        img_label.grid(row=idx, column=0, padx=10, pady=10)
        slide_label = Label(frame, text=f"Slide No. {idx+1}", fg="white", bg="#9b59b6")
        slide_label.grid(row=idx, column=1, padx=10, pady=10)

# Create main window
root = Tk()
root.title("Presentation Timeline")
root.geometry("450x1200")

# Create a canvas to hold the scrollbar and frames
canvas = Canvas(root)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

# Create a frame inside the canvas to hold the images and labels
frame = Frame(canvas, bg="#2c3e50")
canvas.create_window((0, 0), window=frame, anchor='nw')

# Add a scrollbar to the canvas
scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)
canvas.config(yscrollcommand=scrollbar.set)

# Bind the scrolling event
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Call the function to display images
display_images()

root.mainloop()
