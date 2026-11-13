import math
# Indices of the finger tip landmarks (excluding thumb cause I think its not relevant)
FINGER_TIP_INDICES = [8, 12, 16, 20]  
# Threshold for determining if the hand is in a fist position
WRIST_THRESHOLD = 1.0  
def is_hand_fist(pHand_landmarks):
    """
    Determines if the hand is in a fist position based on the landmarks of the hand.

    Args:
        pHand_landmarks: A list of landmarks representing the hand.
    Returns:
        bool: True if the hand is in a fist position, False otherwise.
    """
    # Check if the hand landmarks are provided
    if not pHand_landmarks:
        return False

    distance_wrist_to_middleBase = math.dist(
        (pHand_landmarks[9].x, pHand_landmarks[9].y), 
        (pHand_landmarks[0].x, pHand_landmarks[0].y))

    if distance_wrist_to_middleBase == 0:
        print("Warning: Distance from wrist to middle finger base is zero. Cannot determine fist status.")
        return False  # Avoid division by zero
    # Check if all fingers are folded 
    wrist = pHand_landmarks[0] # wrist landmark
    for finger in FINGER_TIP_INDICES:
        fingerTip = pHand_landmarks[finger]
        tip_wrist_dist = math.dist((fingerTip.x, fingerTip.y), (wrist.x, wrist.y))
        tip_wrist_dist/= distance_wrist_to_middleBase
        if tip_wrist_dist > WRIST_THRESHOLD: # tip is closer to wrist than base
            return False
    return True