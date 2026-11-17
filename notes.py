# notes.py
from config import NUM_ZONES

Ref_frequency = 440                          # C4
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def zone_to_frequency(zone_index: int) -> float:
    """Return the frequency (Hz) of the note for a zone (0 = C ... 11 = B), relative to A4 = 440 Hz."""
    return Ref_frequency * 2 ** ((zone_index - 9) / 12)