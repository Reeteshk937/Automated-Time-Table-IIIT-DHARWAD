import pandas as pd
from pathlib import Path
from scheduler import generate_timetable


# ✅ Step 1 — Load all CSVs
def load_data():
    data_dir = Path("data_templates")
    data = {}
    try:
        data["courses"] = pd.read_csv(data_dir / "course_data.csv")
        data["faculty"] = pd.read_csv(data_dir / "faculty_availability.csv")
        data["classrooms"] = pd.read_csv(data_dir / "classroom_data.csv")
        data["students"] = pd.read_csv(data_dir / "student_data.csv")
        data["exams"] = pd.read_csv(data_dir / "exam_data.csv")
        data["invigilators"] = pd.read_csv(data_dir / "invigilator_data.csv")
        data["constraints"] = pd.read_csv(data_dir / "constraint_data_template.csv")
        data["slots"] = pd.read_csv(data_dir / "slot_mapping_template.csv")
        print("[OK] All CSVs loaded successfully!\n")
    except Exception as e:
        print("[ERROR] Could not load CSVs:", e)
    return data


# ✅ Step 2 — Validate data
def validate_data(data):
    print("[CHECK] Validating data files...\n")
    for name, df in data.items():
        if df.empty:
            print(f"[WARN] {name} file is empty!")
        else:
            print(f"[OK] {name} file loaded — {len(df)} records")

    # Check for important columns
    required = {
        "courses": ["Course Code", "Course Name", "Instructor"],
        "faculty": ["Faculty Name"],
        "classrooms": ["Room Number", "Type", "Capacity"],
        "slots": ["Slot ID", "Day", "Start Time", "End Time"]
    }

    for name, columns in required.items():
        missing = [c for c in columns if c not in data[name].columns]
        if missing:
            print(f"[ERROR] Missing columns in {name}: {missing}")
        else:
            print(f"[OK] {name} columns verified.")
    print("\n[OK] Validation complete!\n")


# ✅ Step 3 — Automatic scheduling
def create_auto_timetable(data):
    print("[RUNNING] Automatic timetable scheduler...\n")
    timetable = generate_timetable(data)
    output_file = "Automated_Timetable.xlsx"
    timetable.to_excel(output_file, index=False)
    print(f"[DONE] Smart timetable created → {output_file}")


if __name__ == "__main__":
    data = load_data()
    validate_data(data)
    create_auto_timetable(data)
