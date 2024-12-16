from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import comtypes.client
import shutil
from PIL import Image
from tkinter.simpledialog import askstring

# Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = "Presentation"
savedPptFolder = "Saved ppt"
annotationPdfFolder = "Annotation PDF"

# Ensure folderPath, savedPptFolder, and annotationPdfFolder exist and are cleared before saving new slides
def ensure_clean_folder(output_folder):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)  # Remove any previous files
    os.makedirs(output_folder)  # Create a new empty folder

# Function to select and upload a PowerPoint file
def upload_ppt():
    Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
    ppt_file = askopenfilename(filetypes=[("PowerPoint files", "*.pptx")], title="Select a PowerPoint file")
    return ppt_file

# Function to convert PowerPoint slides to images using PowerPoint COM
def ppt_to_images_ppt_com(ppt_path, output_folder):
    ensure_clean_folder(output_folder)  # Ensure folder is clean

    # Initialize PowerPoint application
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = 1  # Set PowerPoint to visible mode (optional)

    # Use absolute paths and ensure backslashes for Windows
    ppt_path = os.path.abspath(ppt_path).replace("/", "\\")
    output_folder = os.path.abspath(output_folder).replace("/", "\\")

    print(f"Opening PowerPoint file at: {ppt_path}")
    print(f"Saving images to: {output_folder}")

    try:
        # Open the PowerPoint presentation
        presentation = powerpoint.Presentations.Open(ppt_path)

        # Loop through slides and export them as images
        for i, slide in enumerate(presentation.Slides):
            slide_path = os.path.join(output_folder, f"{i+1}.jpg")
            slide.Export(slide_path, "JPG")
            print(f"Saved slide {i+1} as image: {slide_path}")

        presentation.Close()  # Close the presentation

    except Exception as e:
        print(f"Error processing PowerPoint: {str(e)}")
    
    finally:
        powerpoint.Quit()  # Close PowerPoint application

# Create folders if they don't exist
def create_folders():
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    if not os.path.exists(savedPptFolder):
        os.makedirs(savedPptFolder)
    if not os.path.exists(annotationPdfFolder):
        os.makedirs(annotationPdfFolder)

# Function to save annotated images to "Saved ppt" folder
def save_annotated_images():
    create_folders()
    
    # Get list of presentation images
    pathImages = sorted(os.listdir(folderPath), key=len)
    
    for imgNumber, file_name in enumerate(pathImages):
        if file_name.endswith(".jpg"):
            img_path = os.path.join(folderPath, file_name)
            img = cv2.imread(img_path)
            if img is not None:
                # Apply annotations only to the current slide
                for annotation in annotations:
                    if imgNumber == annotation['slide_number']:
                        for j in range(len(annotation['points'])):
                            if j != 0:
                                cv2.line(img, annotation['points'][j - 1], annotation['points'][j], (0, 0, 200), 12)
                
                save_path = os.path.join(savedPptFolder, file_name)
                cv2.imwrite(save_path, img)

# Function to create a PDF from images in "Saved ppt"
def create_pdf_from_images(image_folder, pdf_folder):
    create_folders()  # Ensure all necessary folders exist
    
    # Get user input for the PDF name
    pdf_name = askstring("Input", "Enter the name for the PDF file (without extension):")
    if not pdf_name:
        print("No name entered. PDF file will not be created.")
        return
    
    pdf_path = os.path.join(pdf_folder, f"{pdf_name}.pdf")
    image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".jpg")])

    images = [Image.open(img).convert("RGB") for img in image_files]
    
    if images:
        images[0].save(pdf_path, save_all=True, append_images=images[1:])
        print(f"PDF created successfully: {pdf_path}")
    else:
        print("No images found to create PDF.")
    
    # Delete all images from "Saved ppt" folder
    for file_name in os.listdir(image_folder):
        file_path = os.path.join(image_folder, file_name)
        os.remove(file_path)
        print(f"Deleted image: {file_path}")

# Main code
ppt_file = upload_ppt()
if ppt_file:
    ppt_to_images_ppt_com(ppt_file, folderPath)

# Initialize video capture
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
delay = 30
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0
annotations = []
annotationNumber = -1
annotationStart = False
hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image

# Get list of presentation images
pathImages = sorted(os.listdir(folderPath), key=len)
print(pathImages)

# Function to resize the image while maintaining aspect ratio
def resize_image(img, target_width, target_height):
    h, w, _ = img.shape
    aspect_ratio = w / h

    # Calculate the new dimensions
    if aspect_ratio > target_width / target_height:
        new_w = target_width
        new_h = int(new_w / aspect_ratio)
    else:
        new_h = target_height
        new_w = int(new_h * aspect_ratio)

    # Create a blank image with the target dimensions
    new_img = np.zeros((target_height, target_width, 3), dtype=np.uint8)
    # Place the resized image in the center of the blank image
    start_x = (target_width - new_w) // 2
    start_y = (target_height - new_h) // 2
    new_img[start_y:start_y + new_h, start_x:start_x + new_w] = cv2.resize(img, (new_w, new_h))
    
    return new_img

# Main loop to display images and detect hand gestures
while True:
    # Get image frame from camera
    success, img = cap.read()
    img = cv2.flip(img, 1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    # Resize the slide image to fit the screen while maintaining aspect ratio
    imgCurrent = resize_image(imgCurrent, width, height)

    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw
    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)

    if hands and not buttonPressed:  # If hand is detected
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingers = detectorHand.fingersUp(hand)  # List of which fingers are up

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations.append({'slide_number': imgNumber, 'points': []})
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations.append({'slide_number': imgNumber, 'points': []})
                    annotationNumber = -1
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if not annotationStart:
                annotationStart = True
                annotationNumber += 1
                annotations.append({'slide_number': imgNumber, 'points': [indexFinger]})
            else:
                annotations[annotationNumber]['points'].append(indexFinger)
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations = [ann for ann in annotations if ann['slide_number'] != imgNumber]
                buttonPressed = True

    else:
        annotationStart = False

    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False

    for annotation in annotations:
        if annotation['slide_number'] == imgNumber:
            for i in range(len(annotation['points'])):
                if i != 0:
                    cv2.line(imgCurrent, annotation['points'][i - 1], annotation['points'][i], (0, 0, 200), 12)

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q') or key == 27:  # 27 is the ASCII value for the Esc key
        break

cap.release()
cv2.destroyAllWindows()

# Save annotated images to "Saved ppt"
save_annotated_images()

# Create PDF from images in "Saved ppt"
create_pdf_from_images(savedPptFolder, annotationPdfFolder)