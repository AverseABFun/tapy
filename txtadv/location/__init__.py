"""Location-related utilites in txtadv. Some of these are copied in modules in txtadv."""
def get_loc_from_num(num):
    """Gets a location string from a number."""
    if num == 0:
        return 'north'
    if num == 1:
        return 'south'
    if num == 2:
        return 'east'
    if num == 3:
        return 'west'
    if num == 4:
        return 'up'
    if num == 5:
        return 'down'
    return 'unknown'


def get_num_from_loc(loc):
    """Gets a number from a location string."""
    loc = loc.lower()
    if loc in ['north', 'n']:
        return 0
    if loc in ['south', 's']:
        return 1
    if loc in ['east', 'e']:
        return 2
    if loc in ['west', 'w']:
        return 3
    if loc in ['up', 'u']:
        return 4
    if loc in ['down', 'd']:
        return 5
    return -1

def loc_dict_to_list(loc: dict) -> list:
    """Converts a location dictionary({'north':room}, for example) to a list"""
    result = [None,None,None,None,None,None]
    for key,value in loc.items():
        num = get_num_from_loc(key)
        if num == -1:
            raise KeyError(f"Invalid key \"{key}\", not a expected direction value")
        result[num] = value
    return result
