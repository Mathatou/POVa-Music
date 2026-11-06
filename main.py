import numpy as np
import cv2 as cv
import mediapipe as mp
import time

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

def on_result(result, output_image: mp.Image, timestamp_ms: int):
    print(f"Detected {len(result.hand_landmarks)} hand(s) at {timestamp_ms} ms")


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    result_callback=on_result,
)

def RenderCamera():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    print("test")
    landmarker = HandLandmarker.create_from_options(options)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = cv.flip(frame, 1) #flip the frame horizontally
        # Convert the BGR image to RGB before processing.
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int(time.monotonic() * 1000)
        landmarker.detect_async(mp_image, timestamp_ms)

                        
        # Display the resulting frame    
        cv.imshow('frame',frame)
        if cv.waitKey(1) == ord('q'): #close on 'q' key
            break
    
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()

def main():
 
    RenderCamera()


if __name__ == "__main__":
    main()