import pandas as pd
import os
from pathlib import Path

# Create data_templates folder if not exists
data_dir = Path("data_templates")
data_dir.mkdir(exist_ok=True)

# 1️⃣ COURSE DATA
course_data = pd.DataFrame([
    {"Course Code": "MA261", "Course Name": "Differential Equations", "Semester": "III",
     "Department": "Mathematics", "LTPSC": "2-0-0-0-2", "Credits": 2,
     "Instructor": "Dr. Anand Barangi", "Registered Students": "",
     "Elective (Yes/No)": "No", "Half Semester (Yes/No)": "No"},
    {"Course Code": "CS261", "Course Name": "Operating System", "Semester": "III",
     "Department": "CSE", "LTPSC": "3-0-0-0-3", "Credits": 3,
     "Instructor": "Dr. Suvadip Hazra", "Registered Students": "",
     "Elective (Yes/No)": "No", "Half Semester (Yes/No)": "No"},
])
course_data.to_csv(data_dir / "course_data.csv", index=False)

# 2️⃣ FACULTY AVAILABILITY
faculty_availability = pd.DataFrame([
    {"Faculty Name": "Dr. Anand Barangi", "Available Days": "Mon-Fri", "Unavailable Time Slots": ""},
    {"Faculty Name": "Dr. Suvadip Hazra", "Available Days": "Mon-Fri", "Unavailable Time Slots": ""},
])
faculty_availability.to_csv(data_dir / "faculty_availability.csv", index=False)

# 3️⃣ CLASSROOM DATA
classroom_data = pd.DataFrame([
    {"Room Number": "C202", "Type": "Classroom", "Capacity": 60, "Facilities": "Projector"},
    {"Room Number": "L101", "Type": "Lab", "Capacity": 30, "Facilities": "Computers"},
])
classroom_data.to_csv(data_dir / "classroom_data.csv", index=False)

# 4️⃣ STUDENT DATA
student_data = pd.DataFrame([
    {"Student Roll Number": "24BCS001", "Name": "Student A", "Department": "CSE",
     "Semester": "III", "Enrolled Courses": "CS261;MA261", "Group": "A", "Special Accommodation": ""},
])
student_data.to_csv(data_dir / "student_data.csv", index=False)

# 5️⃣ EXAM DATA
exam_data = pd.DataFrame([
    {"Course Code": "", "Exam Type": "", "Exam Duration (minutes)": "",
     "Preferred Exam Date": "", "Alternate Exam Date": ""}
])
exam_data.to_csv(data_dir / "exam_data.csv", index=False)

# 6️⃣ INVIGILATOR DATA
invigilator_data = pd.DataFrame([
    {"Invigilator Name": "Dr. Anand Barangi", "Available Days": "Mon-Fri", "Unavailable Time Slots": ""},
])
invigilator_data.to_csv(data_dir / "invigilator_data.csv", index=False)

# 7️⃣ CONSTRAINT DATA
constraint_data = pd.DataFrame([
    {"ConstraintID": "C1", "Type": "BlockLunch", "Subject": "", "Entity": "Time",
     "HardSoft": "HARD", "Details": "12:30-14:00", "PenaltyWeight": 1000},
])
constraint_data.to_csv(data_dir / "constraint_data_template.csv", index=False)

# 8️⃣ SLOT MAPPING
slots = []
days = ["MON", "TUE", "WED", "THU", "FRI"]
slot_times = [
    ("S1", "07:30", "09:00", "Lecture", 1),
    ("S2", "09:00", "10:30", "Lecture", 1),
    ("BRK1", "10:30", "10:45", "Break", 1),
    ("S3", "10:45", "12:15", "Lecture", 1),
    ("LUNCH", "12:30", "14:00", "Lunch", 1),
    ("S4", "14:00", "15:30", "Lecture", 1),
    ("S5", "15:30", "17:00", "Lecture", 1),
]
col_index = 2
for d in days:
    for sid, st, et, typ, span in slot_times:
        slots.append({
            "Slot ID": f"{d}_{sid}",
            "Day": d,
            "ColumnIndex": col_index,
            "Start Time": st,
            "End Time": et,
            "DurationHours": 1.5,
            "Slot Type": typ,
            "Span": span
        })
        col_index += 1
pd.DataFrame(slots).to_csv(data_dir / "slot_mapping_template.csv", index=False)

print("✅ All CSV files successfully created in 'data_templates' folder!")
