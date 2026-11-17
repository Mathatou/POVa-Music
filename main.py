import cv2 as cv
import mediapipe as mp
import time
import os
from config import DEBUG_MODE
from tracking import HandTracker
from display import draw_overlay, draw_current_note
from zones import get_zone_index
from measurements import delete_measurement_files, statistics, writeDataToCSV

def RenderCamera():
    """
    Capture video from the camera, detect hands, and display the video with hand landmarks.
    The function uses the HandTracker class to detect hands in real-time and draws circles on the
    middle finger base of the detected hands. The video feed is displayed in a window, and
    the user can exit the loop by pressing the 'q' key.
    """
    global DEBUG_MODE
    debug = DEBUG_MODE
    measureMode = False
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    tracker = HandTracker()
    try: 
        while True:
            # print(tracker.get_hands())
            # Capture frame-by-frame
            ret, frame = cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                break
            # print(f"capProp: {cap.get(cv.CAP_PROP_FPS)}")
            # Convert the BGR image to RGB before processing.
            rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            tracker.detect(mp_image)
            hands = tracker.get_hands()

            pitch_zone = get_zone_index(hands.pitch.y) if hands.pitch else None
            volume_zone = get_zone_index(hands.volume.y) if hands.volume else None
            frame = cv.flip(frame, 1) #flip the frame horizontally
            if debug is True:
                draw_overlay(frame, hands, pitch_zone, volume_zone)
                draw_current_note(frame, pitch_zone)
            cv.imshow('MusicGen',frame)
            key = cv.waitKey(1)
            if key == ord('q'): #close on 'q' key
                break
            if key == ord('d'): #toggle debug mode on 'd' key
                debug = not debug
                print(f"Debug mode: {debug}")
            if key == ord('x'): #delete all files in measures folder on 'x' key
                delete_measurement_files()
                measureMode = False
                print("All files in measures folder deleted and none will be added.")
    finally:    
        # When everything done, release the capture
        cap.release()
        if measureMode is True:
            data = tracker.measurements
            timeEnd = time.monotonic()*1000
            duration = timeEnd - tracker.timeStart
            duration /= 1000
            print(f"Total duration: {duration:.2f} s")
            print(f"Number of frames: {tracker.nbFrames}")
            os.makedirs(os.path.join(os.getcwd(),'measures'), exist_ok=True)
            writeDataToCSV([{'duration_ms': d} for d in tracker.measurements], 'measures/hand_landmarker_durations.csv')
            statistics(data, tracker.nbFrames, duration)
        tracker.close()
        cv.destroyAllWindows()

def main():
   RenderCamera()


if __name__ == "__main__":
    main()