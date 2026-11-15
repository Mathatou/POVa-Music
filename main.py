import numpy as np
import cv2 as cv
import mediapipe as mp
import time
from config import DEBUG_MODE
from tracking import HandTracker
from display import display_labelsToDraw



def RenderCamera():
    global DEBUG_MODE
    """
    Capture video from the camera, detect hands, and display the video with hand landmarks.
    The function uses the HandTracker class to detect hands in real-time and draws circles on the
    middle finger base of the detected hands. The video feed is displayed in a window, and
    the user can exit the loop by pressing the 'q' key.
    """
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    tracker = HandTracker()
    while True:
        # print(tracker.get_hands())
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        width, height = frame.shape[1], frame.shape[0]
        labelsToDraw = np.array((), dtype=object)
        
        # Convert the BGR image to RGB before processing.
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int(time.monotonic() * 1000)
        tracker.detect(mp_image, timestamp_ms)
        hands = tracker.get_hands()

        frame = cv.flip(frame, 1) #flip the frame horizontally
        if DEBUG_MODE is True:
            display_labelsToDraw(frame, hands, labelsToDraw)
        cv.imshow('MusicGen',frame)
        key = cv.waitKey(1)
        if key == ord('q'): #close on 'q' key
            break
        if key == ord('d'): #toggle debug mode on 'd' key
            DEBUG_MODE = not DEBUG_MODE
            print(f"Debug mode: {DEBUG_MODE}")
    
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

def main():
 
    RenderCamera()


if __name__ == "__main__":
    main()