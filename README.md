# Gesture-Controlled Virtual Keyboard

<img width="2304" height="1407" alt="Opencv Keyboard" src="https://github.com/user-attachments/assets/5d432a52-aaba-4023-8323-aa429bad7a0c" />

An accessible virtual keyboard that lets you type on a computer using only hand gestures detected via a standard webcam. The application displays an on-screen keyboard, tracks the user's hand in real-time, and allows for contactless, intuitive typing in any application.

## Key Features

-   **Real-Time Hand Tracking** - Accurately tracks a single hand's position and key landmarks using the webcam.
-   **Virtual Keyboard Overlay** - Displays a functional 60% keyboard layout directly on the video feed.
-   **Gesture-Based Typing** - Translates a natural thumb-and-index-finger pinch gesture into a keypress.
-   **Intuitive Cursor Control** - The user's index finger acts as the on-screen cursor for selecting keys.
-   **Interactive Visual Feedback** - Keys highlight when hovered over, and the cursor flashes to confirm a click.
-   **System-Wide Integration** - Types into any active application on the computer, from text editors to web browsers.
-   **Performance Optimized** - Tailored to run smoothly on machines with limited processing power.

## Technologies Used

-   **Python 3.10**
-   **OpenCV** - For webcam access and drawing the UI.
-   **MediaPipe** - For the powerful, pre-trained hand tracking model.
-   **PyAutoGUI** - For programmatically controlling the keyboard to simulate key presses.

## Installation & Setup

Follow these steps to get the project running on your local machine.

**1. Prerequisites:**
-   You must have **Python 3.10** installed.
-   You must have a webcam connected to your computer.

**2. Download the Code:**
-   Download the files from this repository.

**3. Install Dependencies:**
-   Open your terminal or command prompt, navigate to the project folder, and install the required libraries from the `requirements.txt` file.

pip install -r requirements.txt

## Usage

1.  Open the application where you want to type (e.g., Notepad, a web browser).
2.  Click inside the text box to make sure it is the active window.
3.  Run the script from your terminal:
    ```
    python virtual_keyboard.py
    ```
4.  A window showing your webcam feed and the virtual keyboard will appear.
5.  **To Type:**
    -   **Hover:** Move your hand to position the green circle (on your index finger) over a key. The key will light up.
    -   **Click:** While hovering, pinch your thumb and index finger together to "press" the key.
6.  Press **'q'** with the keyboard window active to close the program.

## License

This project is licensed under the MIT License.
