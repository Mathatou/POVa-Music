import mediapipe as mp
from dataclasses import dataclass
from typing import Optional
from config import PITCH_HAND, VOLUME_HAND, TASK_MODEL_PATH
from gestures import is_hand_fist

@dataclass
class Hand:
    """
    A dataclass representing a hand with its middle finger base coordinates and fist status.
    Attributes:
        x (float): The x-coordinate of the middle finger base, normalized between 0 and 1.
        y (float): The y-coordinate of the middle finger base, normalized between 0 and 1.
        is_fist (bool): A boolean indicating whether the hand is in a fist position.
    """
    x : float
    y : float
    is_fist : bool

@dataclass
class Hands : 
    """
    A dataclass representing the detected hands for pitch and volume control.
    Attributes:
        pitch (Optional[Hand]): The detected pitch hand, or None if not detected.
        volume (Optional[Hand]): The detected volume hand, or None if not detected.
    """
    pitch  : Optional[Hand]
    volume : Optional[Hand]
      

class HandTracker:
    def __init__(self):
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=TASK_MODEL_PATH),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=2,
            result_callback=self.on_result,
        )
        self.landmarker = HandLandmarker.create_from_options(options)
        self.latest_result = None

    def on_result(self, result, output_image: mp.Image, timestamp_ms: int):
        self.latest_result = result

    def detect(self, mp_image, timestamp_ms):
        """
        Detect hands in the given image.
        Args:
            mp_image (mp.Image): The input image in mediapipe format.
            timestamp_ms (int): The timestamp in milliseconds for the image.
        """
        self.landmarker.detect_async(mp_image, timestamp_ms)
        
    def get_hands(self):
        """
        Get the detected hands and their middle finger base coordinates.
        Returns:
            Hands: A dataclass containing the pitch and volume hands with their coordinates.
        """
        result = self.latest_result
        pitch_hand = None
        volume_hand = None            
        if result is None or not result.hand_landmarks:
            return Hands(pitch=None, volume=None)
        for idx, hand_landmarks in enumerate(result.hand_landmarks):
            handInfo = result.handedness[idx][0]
            hand_label = handInfo.category_name
            middleFingerBase = hand_landmarks[9]  # middle finger base landmark
            
            if hand_label == PITCH_HAND:
                pitch_hand = Hand(x=middleFingerBase.x, y=middleFingerBase.y, is_fist = is_hand_fist(pHand_landmarks=hand_landmarks))
            elif hand_label == VOLUME_HAND:
                volume_hand = Hand(x=middleFingerBase.x, y=middleFingerBase.y, is_fist = is_hand_fist(pHand_landmarks=hand_landmarks))
        return Hands(pitch=pitch_hand, volume=volume_hand)


