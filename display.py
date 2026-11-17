import cv2 as cv
from config import NUM_ZONES
from notes import NOTE_NAMES

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


def _draw_zone_labels(pFrame):
    """Write the note name at the left of each zone (zone 0 is at the bottom)."""
    height = pFrame.shape[0]
    for zone in range(NUM_ZONES):
        row = NUM_ZONES - 1 - zone                    # row 0 = top of the screen
        y = int((row + 0.5) * height / NUM_ZONES)
        cv.putText(pFrame, NOTE_NAMES[zone], (10, y + 6), FONT, 0.6, (255, 255, 255), 1)


def draw_current_note(pFrame, pPitchZone):
    """Show the note currently played, in large text at the top right."""
    width = pFrame.shape[1]
    text = NOTE_NAMES[pPitchZone] if pPitchZone is not None else "-"
    (text_w, _), _ = cv.getTextSize(text, FONT, 2, 3)
    cv.putText(pFrame, text, (width - text_w - 20, 60), FONT, 2, (0, 255, 255), 3)


def _hand_text(pName, pZone, pHand):
    """Build the debug label for a hand and its current zone."""
    state = "fist" if pHand.is_fist else "open"
    note = f" [{NOTE_NAMES[pZone]}]" if pName == "Pitch" and pZone is not None else ""
    return f"{pName} zone: {pZone} ({state})"


def draw_overlay(pFrame, pHands, pPitchZone, pVolumeZone):
    """
    Draw the complete debug overlay on an already flipped frame.

    ``pPitchZone`` and ``pVolumeZone`` may be ``None`` when the corresponding
    hand is not detected. The function only draws the supplied information.
    """
    _draw_zone_lines(pFrame)
    _draw_zone_labels(pFrame)

    lines = ["Press 'q' to quit", "Press 'd' to toggle debug mode"]
    if pHands.pitch:
        _draw_hand(pFrame, pHands.pitch, PITCH_COLORS)
        lines.append(_hand_text("Pitch", pPitchZone, pHands.pitch))
    if pHands.volume:
        _draw_hand(pFrame, pHands.volume, VOLUME_COLORS)
        lines.append(_hand_text("Volume", pVolumeZone, pHands.volume))


    for i, line in enumerate(lines):
        cv.putText(pFrame, line, (50, 25 + i * 25), FONT, 0.6, (0, 255, 0), 2)