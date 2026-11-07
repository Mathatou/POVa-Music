from config import NUM_ZONES
def get_zone_index(y,pHeight_per_zone):

    zone_index = NUM_ZONES - 1 - int(y / pHeight_per_zone)
    zone_index = max(0, min(zone_index, NUM_ZONES - 1))

    return zone_index