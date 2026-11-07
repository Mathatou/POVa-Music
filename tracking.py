import mediapipe as mp
from dataclasses import dataclass
from typing import Optional
from config import PITCH_HAND, VOLUME_HAND

@dataclass
class Hand:
    x : float
    y : float
    is_fist : bool

@dataclass
class Hands : 
    pitch  : Optional[Hand]
    volume : Optional[Hand]
      

class HandTracker:
    def __init__(self):
        BaseOptions = mp.tasks.BaseOptions
        HandLandmarker = mp.tasks.vision.HandLandmarker
        HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        VisionRunningMode = mp.tasks.vision.RunningMode
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
            running_mode=VisionRunningMode.LIVE_STREAM,
            num_hands=2,
            result_callback=self.on_result,
        )
        self.landmarker = HandLandmarker.create_from_options(options)
        self.latest_result = None

    def on_result(self, result, output_image: mp.Image, timestamp_ms: int):
        self.latest_result = result

    def detect(self, mp_image, timestamp_ms):
        self.landmarker.detect_async(mp_image, timestamp_ms)
        
    def get_hands(self):
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
                pitch_hand = Hand(x=middleFingerBase.x, y=middleFingerBase.y, is_fist=False)  # Placeholder for is_fist logic
            elif hand_label == VOLUME_HAND:
                volume_hand = Hand(x=middleFingerBase.x, y=middleFingerBase.y, is_fist=False)  # Placeholder for is_fist logic
        return Hands(pitch=pitch_hand, volume=volume_hand)


