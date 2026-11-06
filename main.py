import numpy as np
import cv2 as cv

def RenderCamera():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    print("test")
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = cv.flip(frame, 1) #flip the frame horizontally
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
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