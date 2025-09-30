def create_room(room_number, capacity, type_="Lecture"):
    """
    Create a room dictionary.
    """
    return {
        "room_number": room_number,
        "capacity": capacity,
        "type": type_
    }
