import numpy as np
import cv2 as cv
import mediapipe as mp
import time
from config import NUM_ZONES
from tracking import HandTracker, Hands, Hand


def RenderCamera():
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
        print(tracker.get_hands())
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

        if hands.pitch:
            pitchCoord = (int(hands.pitch.x * width), int(hands.pitch.y * height))
            if hands.pitch.is_fist:
                color = (255, 120, 255)
            else:
                color = (0, 255, 0)
            cv.circle(frame, pitchCoord, 5, color, -1) # green for pitch (left) hand

        if hands.volume:
            volumeCoord = (int(hands.volume.x * width), int(hands.volume.y * height))
            if hands.volume.is_fist:
                color = (255, 0, 255)
            else:
                color = (255, 0, 0)
            cv.circle(frame, volumeCoord, 5, color, -1) # blue for volume (right) hand
        # Display the resulting frame    
        frame = cv.flip(frame, 1) #flip the frame horizontally

        cv.putText(frame, "Press 'q' to quit", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if labelsToDraw.size > 0:
            cv.putText(frame,labelsToDraw[0], (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.imshow('MusicGen',frame)
        if cv.waitKey(1) == ord('q'): #close on 'q' key
            break
    
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

def main():
 
    RenderCamera()


if __name__ == "__main__":
    main()