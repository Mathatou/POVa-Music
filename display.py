import cv2 as cv
from config import NUM_ZONES

FONT = cv.FONT_HERSHEY_SIMPLEX
# Couleurs en BGR (ordre OpenCV) : (ouverte, poing)
PITCH_COLORS = ((0, 255, 0), (255, 120, 255))
VOLUME_COLORS = ((255, 0, 0), (255, 0, 255))


def _draw_zone_lines(pFrame):
    """Draw horizontal lines that divide the frame into configured zones."""
    height, width = pFrame.shape[:2]
    for i in range(1, NUM_ZONES):
        y = int(i * height / NUM_ZONES)
        cv.line(pFrame, (0, y), (width, y), (255, 255, 255), 1)


def _draw_hand(pFrame, pHand, pColors):
    """Draw a hand marker using its normalized coordinates and state color."""
    height, width = pFrame.shape[:2]
    x = width - 1 - int(pHand.x * width)
    y = int(pHand.y * height)
    color = pColors[1] if pHand.is_fist else pColors[0]
    cv.circle(pFrame, (x, y), 8, color, -1)


def _hand_text(pName, pZone, pHand):
    """Build the debug label for a hand and its current zone."""
    state = "fist" if pHand.is_fist else "open"
    return f"{pName} zone: {pZone} ({state})"


def draw_overlay(pFrame, pHands, pPitchZone, pVolumeZone):
    """
    Draw the complete debug overlay on an already flipped frame.

    ``pPitchZone`` and ``pVolumeZone`` may be ``None`` when the corresponding
    hand is not detected. The function only draws the supplied information.
    """
    _draw_zone_lines(pFrame)

    lines = ["Press 'q' to quit", "Press 'd' to toggle debug mode"]
    if pHands.pitch:
        _draw_hand(pFrame, pHands.pitch, PITCH_COLORS)
        lines.append(_hand_text("Pitch", pPitchZone, pHands.pitch))
    if pHands.volume:
        _draw_hand(pFrame, pHands.volume, VOLUME_COLORS)
        lines.append(_hand_text("Volume", pVolumeZone, pHands.volume))

    for i, line in enumerate(lines):
        cv.putText(pFrame, line, (10, 25 + i * 25), FONT, 0.6, (0, 255, 0), 2)