import numpy as np
import cv2 as cv
import mediapipe as mp
import time

PITCH_HAND = "Left"
VOLUME_HAND = "Right"
NUM_ZONES = 12
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
latest_result = None

def on_result(result, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    if latest_result is not None:
        pass
    latest_result = result


options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    num_hands=2,
    result_callback=on_result,
)

def RenderCamera():
    global latest_result
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
        width, height = frame.shape[1], frame.shape[0]
        height_per_zone = height / NUM_ZONES
        
        # Convert the BGR image to RGB before processing.
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp_ms = int(time.monotonic() * 1000)
        landmarker.detect_async(mp_image, timestamp_ms)

        if latest_result is not None and latest_result.hand_landmarks:
            for idx, hand_landmarks in enumerate(latest_result.hand_landmarks):
                handInfo = latest_result.handedness[idx][0]
                hand_label = handInfo.category_name
                score = handInfo.score
                middleFingerBase = hand_landmarks[9]  # middle finger base landmark
                middleFingerBaseCoords = (int(middleFingerBase.x * width), int(middleFingerBase.y * height))    
                cv.circle(frame,middleFingerBaseCoords, 5, (0,255,0),-1) #draw a circle on the first landmark of the first hand
                for i in range(NUM_ZONES): # Get rid of ? 
                    y = int(i * height_per_zone)
                    cv.line(frame, (0, y), (width, y), (255, 0, 0), 1)  # Draw horizontal lines for zones
                zone_index = NUM_ZONES - int(middleFingerBaseCoords[1] / height_per_zone)
                zone_index = max(0, min(zone_index, NUM_ZONES - 1))
                # print(f"Hand {idx}: {hand_label} ({score:.2f}) is in zone {zone_index+1}")

                if hand_label == PITCH_HAND:
                    # Handle pitch control logic here
                    print("Pitch control activated")
                    pass
                elif hand_label == VOLUME_HAND:
                    # Handle volume control logic here
                    print("Volume control activated")
                    pass

        # Display the resulting frame    
        frame = cv.flip(frame, 1) #flip the frame horizontally
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