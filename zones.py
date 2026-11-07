from config import NUM_ZONES

def get_zone_index(y):
    """
    Get the zone index based on the y-coordinate of the middle finger base.
    The y-coordinate should be normalized between 0 and 1, where 0 is the top of the image and 1 is the bottom.
    
    Args : 
        y (float): The normalized y-coordinate of the point (between 0 and 1).
    Returns :
        int: The index of the zone that the point falls into, clamped between 0 and NUM_ZONES - 1.

    """
    zone_index = NUM_ZONES - 1 - int(y * NUM_ZONES)
    zone_index = max(0, min(zone_index, NUM_ZONES - 1))
    return zone_index

if __name__ == "__main__":
    print(get_zone_index(0.0), get_zone_index(0.5), get_zone_index(1.0))