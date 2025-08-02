import cv2
import mediapipe as mp
import pyautogui
import math
import time

# --- SETTINGS ---
# Performance settings
WEBCAM_WIDTH = 1920
WEBCAM_HEIGHT = 1080

# Usability settings
# NOTE: The distance for a thumb-and-index pinch might be slightly larger
CLICK_DISTANCE_THRESHOLD = 30  # Increased slightly for the thumb gesture
CLICK_COOLDOWN_SECONDS = 0.5   # Prevents rapid, accidental double-clicks

# --- INITIALIZATION ---
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, WEBCAM_WIDTH)
cap.set(4, WEBCAM_HEIGHT)

screen_width, screen_height = pyautogui.size()

# --- 60% KEYBOARD LAYOUT ---
# Define key properties
KEY_WIDTH, KEY_HEIGHT = 80, 80
KEY_MARGIN = 20
KEY_FONT_SCALE = 2
KEY_FONT_THICKNESS = 3

# Define colors (B, G, R)
COLOR_KEY = (100, 50, 0)
COLOR_KEY_HOVER = (150, 100, 0)
COLOR_KEY_TEXT = (255, 255, 255)
COLOR_CURSOR_BODY = (0, 255, 0)
COLOR_CURSOR_CLICK = (0, 0, 255)

# Special keys for pyautogui must be in lowercase (e.g., 'backspace', 'enter')
key_layout = [
    ["`", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "backspace"],
    ["tab", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "\\"],
    ["caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "enter"],
    ["shift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "shift"],
    ["space"]
]

# Dynamically generate key objects based on the layout
keys = []
for row_idx, row in enumerate(key_layout):
    for col_idx, key_char in enumerate(row):
        x = col_idx * (KEY_WIDTH + KEY_MARGIN) + KEY_MARGIN
        y = row_idx * (KEY_HEIGHT + KEY_MARGIN) + KEY_MARGIN
        
        # Make spacebar wider
        width = KEY_WIDTH * 4 if key_char == "space" else KEY_WIDTH
        
        # Store key info as a dictionary for clarity
        keys.append({
            "char": key_char,
            "x": x, "y": y,
            "w": width, "h": KEY_HEIGHT
        })

# --- FUNCTIONS ---
def draw_keyboard(image, keys, hovered_key_char):
    """Draws the keyboard buttons, highlighting the hovered key."""
    for key in keys:
        x, y, w, h = key["x"], key["y"], key["w"], key["h"]
        char = key["char"].upper()

        # Choose color based on hover state
        bg_color = COLOR_KEY_HOVER if key["char"] == hovered_key_char else COLOR_KEY
        cv2.rectangle(image, (x, y), (x + w, y + h), bg_color, cv2.FILLED)
        
        # Center the text on the key
        text_size = cv2.getTextSize(char, cv2.FONT_HERSHEY_PLAIN, KEY_FONT_SCALE, KEY_FONT_THICKNESS)[0]
        text_x = x + (w - text_size[0]) // 2
        text_y = y + (h + text_size[1]) // 2
        cv2.putText(image, char, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, KEY_FONT_SCALE, COLOR_KEY_TEXT, KEY_FONT_THICKNESS)


# --- MAIN LOOP ---
last_click_time = 0
hovered_key_char = None

while True:
    success, image = cap.read()
    if not success:
        break

    image = cv2.flip(image, 1)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    # Reset hover state each frame
    hovered_key_char = None

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
        # --- MODIFICATION START ---
        # Get landmark coordinates for index finger and THUMB
        index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP] # Changed from MIDDLE_FINGER_TIP
        
        # Convert landmark coordinates to pixel coordinates on the WEBCAM frame
        ix_cam, iy_cam = int(index_tip.x * WEBCAM_WIDTH), int(index_tip.y * WEBCAM_HEIGHT)
        tx_cam, ty_cam = int(thumb_tip.x * WEBCAM_WIDTH), int(thumb_tip.y * WEBCAM_HEIGHT) # New variables for thumb
        # --- MODIFICATION END ---

        # Map index finger position to the FULL SCREEN for cursor control
        cursor_x = int(index_tip.x * screen_width)
        cursor_y = int(index_tip.y * screen_height)
        
        # Check for key hover using the webcam frame coordinates
        for key in keys:
            if key["x"] < ix_cam < key["x"] + key["w"] and key["y"] < iy_cam < key["y"] + key["h"]:
                hovered_key_char = key["char"]
                break

        # --- MODIFICATION START ---
        # Calculate distance for click gesture between index finger and THUMB
        distance = math.hypot(ix_cam - tx_cam, iy_cam - ty_cam) # Changed to use thumb coordinates
        # --- MODIFICATION END ---
        cursor_color = COLOR_CURSOR_BODY

        # Check for click gesture and cooldown
        if distance < CLICK_DISTANCE_THRESHOLD and (time.time() - last_click_time) > CLICK_COOLDOWN_SECONDS:
            if hovered_key_char is not None:
                # A click happened on a key!
                pyautogui.press(hovered_key_char)
                last_click_time = time.time()
                cursor_color = COLOR_CURSOR_CLICK # Show click feedback
                
    # Draw all components
    draw_keyboard(image, keys, hovered_key_char)

    # Draw the visual cursor on the hand (after drawing the keyboard)
    if results.multi_hand_landmarks:
        cv2.circle(image, (ix_cam, iy_cam), 10, cursor_color, cv2.FILLED)

    cv2.imshow("Virtual Keyboard", image)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# --- CLEANUP ---
cap.release()
cv2.destroyAllWindows()
