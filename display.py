import cv2 as cv
import numpy as np
from zones import get_zone_index
from config import NUM_ZONES


def display_zones(pFrame, pWidth, pHeight):
    for i in range(1, NUM_ZONES):
        cv.line(pFrame, (0, int(pHeight / NUM_ZONES) * i), (pWidth, int(pHeight / NUM_ZONES) * i), (255, 255, 255), 2)


def display_hands(pHands, pWidth, pHeight, pFrame, pLabelsToDraw):
    if pHands.pitch:
        pitchCoord = (pWidth-1-int(pHands.pitch.x * pWidth), int(pHands.pitch.y * pHeight))
        if pHands.pitch.is_fist:
            color = (255, 120, 255)
        else:
            color = (0, 255, 0)
        cv.circle(pFrame, pitchCoord, 5, color, -1) # green for pitch (left) hand

        pLabelsToDraw = np.append(pLabelsToDraw, f"Pitch Zone: {get_zone_index(pHands.pitch.y)}")
    if pHands.volume:
        volumeCoord = (pWidth-1-int(pHands.volume.x * pWidth), int(pHands.volume.y * pHeight))
        if pHands.volume.is_fist:
            color = (255, 0, 255)
        else:
            color = (255, 0, 0)
        cv.circle(pFrame, volumeCoord, 5, color, -1) # blue for volume (right) hand
        pLabelsToDraw = np.append(pLabelsToDraw, f"Volume Zone: {get_zone_index(pHands.volume.y)}")
            
    return pLabelsToDraw


def display_options(pFrame):
    cv.putText(pFrame, "Press 'q' to quit", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv.putText(pFrame, "Press 'd' to toggle debug mode", (10, 60), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

def display_labelsToDraw(pFrame, pHands, pLabelsToDraw):
    if pLabelsToDraw.size > 0:
        for i, label in enumerate(pLabelsToDraw):
            cv.putText(pFrame, label, (10, 70 + i * 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    display_options(pFrame)
    display_zones(pFrame, pFrame.shape[1], pFrame.shape[0])
    pLabelsToDraw = np.append(pLabelsToDraw, display_hands(pHands, pFrame.shape[1], pFrame.shape[0], pFrame, pLabelsToDraw))