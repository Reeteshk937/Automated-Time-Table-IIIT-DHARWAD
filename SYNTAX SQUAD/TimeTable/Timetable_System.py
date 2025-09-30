from timetable.utils import load_data

def generate_timetable(courses, faculty, rooms):
    """
    Generate a simple timetable (dummy logic).
    Each course assigned a faculty, room, and time slot.
    """
    timetable = []
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]

    i = 0
    for course in courses:
        fac = faculty[i % len(faculty)]
        room = rooms[i % len(rooms)]
        day = days[i % len(days)]
        slot = f"{day} 10:00-11:00"

        entry = {
            "course": course["name"],
            "faculty": fac["name"],
            "room": room["room_number"],
            "slot": slot
        }
        timetable.append(entry)
        i += 1

    return timetable
