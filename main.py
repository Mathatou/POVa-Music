import numpy as np
import cv2 as cv
import mediapipe as mp
import time
from config import DEBUG_MODE
from tracking import HandTracker
from display import draw_overlay, draw_current_note
from zones import get_zone_index
import os 
from notes import NOTE_NAMES, zone_to_frequency


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
    while True:
        # print(tracker.get_hands())
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
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
        cv.imshow('MusicGen',frame)
        key = cv.waitKey(1)
        if key == ord('q'): #close on 'q' key
            break
        if key == ord('d'): #toggle debug mode on 'd' key
            debug = not debug
            print(f"Debug mode: {debug}")
    
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

def _next_available_filename(filename):
    base, extension = os.path.splitext(filename)
    candidate = filename
    counter = 0
    while os.path.exists(candidate):
        counter += 1
        candidate = f"{base}_{counter}{extension}"
    return candidate


def writeDataToCSV(data, filename):
    import csv
    filename = _next_available_filename(filename)
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['duration_ms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)



def statistics(data, frameNmb, duration):
    """
    Calculate and print basic statistics (mean, median, min, max) for a list of numerical data.
    
    Args:
        data (list): A list of numerical values.
    """
    if not data:
        print("No data provided for statistics.")
        return
    filename = _next_available_filename('measures/hand_landmarker_statistics.txt')
    mean = np.mean(data)
    median = np.median(data)
    min_val = np.min(data)
    max_val = np.max(data)
    percentile_95 = np.percentile(data, 95)
    with open(filename, 'w') as f:
        f.write(f"Statistics:\n")
        f.write(f"Mean: {mean:.2f} ms\n")
        f.write(f"Median: {median:.2f} ms\n")
        f.write(f"Min: {min_val:.2f} ms\n")
        f.write(f"Max: {max_val:.2f} ms\n")
        f.write(f"95th Percentile: {percentile_95:.2f} ms\n")
        f.write(f"Number of Frames sent: {frameNmb}\n")
        f.write(f"Number of Frames received: {len(data)}\n")
        f.write(f"Number of Frames lost: {frameNmb - len(data)}\n")
        f.write(f"Total Duration: {duration:.2f} s\n")
        f.write(f"Average FPS: {frameNmb/duration:.2f} fps\n")
    
def delete_measurement_files():
    """
    Delete all files in the 'measures' directory.
    """
    measures_dir = 'measures'
    if os.path.exists(measures_dir):
        for filename in os.listdir(measures_dir):
            file_path = os.path.join(measures_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")

def main():
   RenderCamera()


if __name__ == "__main__":
    main()