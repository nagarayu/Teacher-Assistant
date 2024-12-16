from tkinter import *
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer as pdf
import os

# Create the main window
root = Tk()
root.geometry("1300x1000+400+100")  # Adjust window size
root.title("PDF Viewer")
root.configure(bg="#eaeaea")

# Function to browse and display the PDF
def browseFiles():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select PDF file",
                                          filetype=(("PDF File", "*.pdf"), 
                                                    ("All Files", "*.*")))
    if filename:
        v1 = pdf.ShowPdf()
        # Set width and height to fit the window
        v2 = v1.pdf_view(root, pdf_location=open(filename, "r"), width=200, height=1000)
        v2.pack(pady=(0, 0))

# Create a button to open PDFs
Button(root, text="Open PDF", command=browseFiles, width=40, font="arial 20", bd=4).pack()

# Start the Tkinter event loop
root.mainloop()
