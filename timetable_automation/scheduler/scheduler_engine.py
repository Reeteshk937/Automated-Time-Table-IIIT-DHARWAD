def find_room_for(course_row, rooms_df, session_type):
    """Find a suitable room based on type and capacity."""
    for _, r in rooms_df.iterrows():
        room_type = str(r.get("Type", "")).strip().lower()
        if session_type == "Lab" and "lab" not in room_type:
            continue
        if session_type == "Lecture" and "class" not in room_type:
            continue

        # Check capacity if exists
        try:
            if int(r.get("Capacity", 0)) < int(course_row.get("Registered Students", 0) or 0):
                continue
        except:
            pass

        # Room found
        return r.get("Room Number") or r.get("Name") or "Unknown"
    return None
