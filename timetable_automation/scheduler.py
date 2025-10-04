import pandas as pd
import random

def generate_timetable(data):
    """
    Automatically assigns courses into a timetable grid (Days × Slots like A1, B1, L1, etc.)
    """
    courses = data["courses"]
    rooms = data["classrooms"]
    slots = data["slots"]

    timetable = []
    used_slots = set()
    faculty_busy = set()

    # Creating a list of course sessions based on their LTPSC
    course_sessions = []
    for _, course in courses.iterrows():
        L, T, P, S, C = map(int, course["LTPSC"].split("-"))
        sessions = []
        for _ in range(L):
            sessions.append({"course": course["Course Code"], "type": "Lecture", "instructor": course["Instructor"]})
        for _ in range(T):
            sessions.append({"course": course["Course Code"], "type": "Tutorial", "instructor": course["Instructor"]})
        for _ in range(P):
            sessions.append({"course": course["Course Code"], "type": "Lab", "instructor": course["Instructor"]})
        course_sessions.extend(sessions)

    # Assign sessions to slots
    for session in course_sessions:
        assigned = False
        attempts = 0
        while not assigned and attempts < 50:
            attempts += 1
            slot = slots.sample(1).iloc[0]
            slot_id = slot["Slot ID"]
            day = slot["Day"]
            start_time = slot["Start Time"]
            room = rooms.sample(1).iloc[0]

            # Check constraints to ensure no overbooking
            if (day, slot_id, room["Room Number"]) in used_slots:
                continue
            if (day, slot_id, session["instructor"]) in faculty_busy:
                continue
            if session["type"] == "Lab" and room["Type"] != "Lab":
                continue
            if session["type"] in ["Lecture", "Tutorial"] and room["Type"] != "Classroom":
                continue

            # Assign session to slot
            timetable.append({
                "Day": day,
                "Slot ID": slot_id,
                "Course Code": session["course"],
                "Instructor": session["instructor"],
                "Room": room["Room Number"],
            })
            used_slots.add((day, slot_id, room["Room Number"]))
            faculty_busy.add((day, slot_id, session["instructor"]))
            assigned = True

    # Create DataFrame for the timetable
    df = pd.DataFrame(timetable)

    # ---- Build Grid (matching the second image structure) ----
    # Define the time slots for each day (the rows will be time slots, the columns will be the days)
    time_slots = [
        "09:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", 
        "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"
    ]
    
    days = ["MON", "TUE", "WED", "THU", "FRI"]
    grid = pd.DataFrame(index=time_slots, columns=days)

    # Iterate through timetable and assign each course to the correct time slot
    for _, row in df.iterrows():
        time_slot = row["Slot ID"]  # Assuming Slot ID corresponds to time slot
        day = row["Day"]
        grid.at[time_slot, day] = f"{row['Course Code']} ({row['Room']})"
    
    # Fill missing values with empty strings for clarity
    grid = grid.fillna("")

    return grid

# Example Data to Use in the Function
courses_data = pd.DataFrame({
    "Course Code": ["CS261", "MA261", "PHY101", "CS101", "BIO102"],
    "Instructor": ["Dr. A", "Dr. B", "Dr. C", "Dr. D", "Dr. E"],
    "LTPSC": ["3-1-0-0-0", "3-0-1-0-0", "2-1-1-0-0", "4-0-0-0-0", "3-0-1-0-0"]
})

classrooms_data = pd.DataFrame({
    "Room Number": ["101", "102", "103", "104", "105"],
    "Type": ["Classroom", "Classroom", "Lab", "Lab", "Classroom"]
})

slots_data = pd.DataFrame({
    "Slot ID": [0, 1, 2, 3, 4, 5, 6, 7, 8],
    "Day": ["MON", "TUE", "WED", "THU", "FRI", "MON", "TUE", "WED", "THU"],
    "Start Time": ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00"]
})

# Generate the timetable
data = {"courses": courses_data, "classrooms": classrooms_data, "slots": slots_data}
final_timetable = generate_timetable(data)

# Show the final timetable
print(final_timetable)