import math
# Indices of the finger tip landmarks
FINGER_TIP_INDICES = [4, 8, 12, 16, 20]
THUMB_IP_INDEX = 3
INDEX_MCP_INDEX = 5
# Threshold for determining if the hand is in a fist position
WRIST_THRESHOLD = 1.0  
def is_hand_closed(pHand_landmarks):
    """
    Determines if the hand is in a fist position based on the landmarks of the hand.

    Args:
        pHand_landmarks: A list of landmarks representing the hand.
    Returns:
        tuple[bool, int]: Whether the hand is in a fist position and the
            number of raised fingers.
    """
    howManyFingersUp = 0
    # Check if the hand landmarks are provided
    if not pHand_landmarks:
        return False, howManyFingersUp

    distance_wrist_to_middleBase = math.dist(
        (pHand_landmarks[9].x, pHand_landmarks[9].y), 
        (pHand_landmarks[0].x, pHand_landmarks[0].y))

    if distance_wrist_to_middleBase == 0:
        print("Warning: Distance from wrist to middle finger base is zero. Cannot determine fist status.")
        return False, howManyFingersUp  # Avoid division by zero

    # The thumb bends differently from the other fingers. Comparing both
    # thumb joints with the index MCP works for either hand orientation.
    wrist = pHand_landmarks[0]
    for finger in FINGER_TIP_INDICES:
        fingerTip = pHand_landmarks[finger]
        if finger == 4:  # Thumb
            thumbIp = pHand_landmarks[THUMB_IP_INDEX]
            indexMcp = pHand_landmarks[INDEX_MCP_INDEX]
            thumb_tip_index_dist = math.dist(
                (fingerTip.x, fingerTip.y), (indexMcp.x, indexMcp.y)
            )
            thumb_ip_index_dist = math.dist(
                (thumbIp.x, thumbIp.y), (indexMcp.x, indexMcp.y)
            )
            if thumb_tip_index_dist > thumb_ip_index_dist:
                howManyFingersUp += 1
            continue

        tip_wrist_dist = math.dist((fingerTip.x, fingerTip.y), (wrist.x, wrist.y))
        tip_wrist_dist /= distance_wrist_to_middleBase
        if tip_wrist_dist > WRIST_THRESHOLD:
            howManyFingersUp += 1

    return howManyFingersUp == 0, howManyFingersUp