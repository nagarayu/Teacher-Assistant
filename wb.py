import mediapipe as mp
import cv2
import numpy as np
import time
import os


# Constants
ml = 150  # Margin left for tools area
max_x, max_y = 250 + ml, 50  # Max bounds for tools area
curr_tool = "select tool"
time_init = True
rad = 40
var_inits = False
thick = 4
prevx, prevy = 0, 0

# Get tools function
def getTool(x):
    if x < 50 + ml:
        return "line"
    elif x < 100 + ml:
        return "rectangle"
    elif x < 150 + ml:
        return "draw"
    elif x < 200 + ml:
        return "circle"
    else:
        return "erase"

def index_raised(yi, y9):
    return (y9 - yi) > 40

hands = mp.solutions.hands
hand_landmark = hands.Hands(min_detection_confidence=0.6, min_tracking_confidence=0.6, max_num_hands=1)
draw = mp.solutions.drawing_utils

# Load tools image
tools_path = "tools.png"
tools = cv2.imread(tools_path)
if tools is None:
    print(f"Error: {tools_path} not found or cannot be read.")
    tools = np.zeros((max_y + 5, max_x + 5, 3), dtype="uint8")
else:
    tools = tools.astype('uint8')

# Mask to hold the drawings
mask = np.ones((480, 640), dtype="uint8") * 255

# Another mask for persistent drawing
persistent_mask = np.ones((480, 640, 3), dtype="uint8") * 255

cap = cv2.VideoCapture(0)

# Set the window to be resizable for full-screen capability
cv2.namedWindow("paint app", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("paint app", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)

    op = hand_landmark.process(rgb)

    # Create a full-screen white background (now set to light gray #eaeaea)
    white_background = np.ones_like(frm, dtype="uint8") * 234  # Light gray background

    if op.multi_hand_landmarks:
        for i in op.multi_hand_landmarks:
            # Get the fingertip coordinates
            x, y = int(i.landmark[8].x * frm.shape[1]), int(i.landmark[8].y * frm.shape[0])

            # Draw landmarks and finger pointer
            draw.draw_landmarks(white_background, i, hands.HAND_CONNECTIONS)
            cv2.circle(white_background, (x, y), rad, (0, 0, 255), -1)  # Red circle for the fingertip

            # Detect if the tool should change based on the fingertip position
            if x < max_x and y < max_y and x > ml:
                if time_init:
                    ctime = time.time()
                    time_init = False
                ptime = time.time()

                cv2.circle(white_background, (x, y), rad, (0, 255, 255), 2)
                rad -= 1

                if (ptime - ctime) > 0.8:
                    curr_tool = getTool(x)
                    print("Your current tool set to:", curr_tool)
                    time_init = True
                    rad = 40
            else:
                time_init = True
                rad = 40

            # Draw on the persistent mask based on selected tool
            if curr_tool == "draw":
                xi, yi = int(i.landmark[12].x * frm.shape[1]), int(i.landmark[12].y * frm.shape[0])
                y9 = int(i.landmark[9].y * frm.shape[0])

                if index_raised(yi, y9):
                    cv2.line(persistent_mask, (prevx, prevy), (x, y), (0, 0, 0), thick)
                    prevx, prevy = x, y
                else:
                    prevx = x
                    prevy = y

            elif curr_tool == "line":
                xi, yi = int(i.landmark[12].x * frm.shape[1]), int(i.landmark[12].y * frm.shape[0])
                y9 = int(i.landmark[9].y * frm.shape[0])

                if index_raised(yi, y9):
                    if not var_inits:
                        xii, yii = x, y
                        var_inits = True
                    cv2.line(white_background, (xii, yii), (x, y), (50, 152, 255), thick)
                else:
                    if var_inits:
                        cv2.line(persistent_mask, (xii, yii), (x, y), (0, 0, 0), thick)
                        var_inits = False

            elif curr_tool == "rectangle":
                xi, yi = int(i.landmark[12].x * frm.shape[1]), int(i.landmark[12].y * frm.shape[0])
                y9 = int(i.landmark[9].y * frm.shape[0])

                if index_raised(yi, y9):
                    if not var_inits:
                        xii, yii = x, y
                        var_inits = True
                    cv2.rectangle(white_background, (xii, yii), (x, y), (0, 255, 255), thick)
                else:
                    if var_inits:
                        cv2.rectangle(persistent_mask, (xii, yii), (x, y), (0, 0, 0), thick)
                        var_inits = False

            elif curr_tool == "circle":
                xi, yi = int(i.landmark[12].x * frm.shape[1]), int(i.landmark[12].y * frm.shape[0])
                y9 = int(i.landmark[9].y * frm.shape[0])

                if index_raised(yi, y9):
                    if not var_inits:
                        xii, yii = x, y
                        var_inits = True
                    cv2.circle(white_background, (xii, yii), int(((xii - x)**2 + (yii - y)**2)**0.5), (255, 255, 0), thick)
                else:
                    if var_inits:
                        cv2.circle(persistent_mask, (xii, yii), int(((xii - x)**2 + (yii - y)**2)**0.5), (0, 0, 0), thick)
                        var_inits = False

            elif curr_tool == "erase":
                xi, yi = int(i.landmark[12].x * frm.shape[1]), int(i.landmark[12].y * frm.shape[0])
                y9 = int(i.landmark[9].y * frm.shape[0])

                if index_raised(yi, y9):
                    cv2.circle(white_background, (x, y), 30, (234, 234, 234), -1)
                    cv2.circle(persistent_mask, (x, y), 30, (234, 234, 234), -1)

    # Apply the persistent drawing over the white background
    white_background = cv2.bitwise_and(persistent_mask, white_background)

    # Place the tool image on top of the white background
    white_background[:max_y, ml:max_x] = cv2.addWeighted(tools, 0.7, white_background[:max_y, ml:max_x], 0.3, 0)

    # Display the current tool
    cv2.putText(white_background, curr_tool, (270 + ml, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


    # Adding text to the bottom right corner
    text = "Teacher's Assistant"
    font = cv2.FONT_HERSHEY_COMPLEX  # Use a different font style for a more italic look
    font_scale = 0.5  # Smaller font size
    color = (0, 0, 0)  # Text color in BGR format for "#eaeaea"
    thickness = 1

    # Calculate the position for bottom-right corner
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = white_background.shape[1] - text_size[0] - 10  # 10 pixels padding from right
    text_y = white_background.shape[0] - 10  # 10 pixels padding from bottom

    # Put the text in the bottom right corner
    cv2.putText(white_background, text, (text_x, text_y), font, font_scale, color, thickness)


    
    # Show the final output
    cv2.imshow("paint app", white_background)

    

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break
