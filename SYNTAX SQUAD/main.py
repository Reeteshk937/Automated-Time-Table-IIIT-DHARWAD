from timetable.timetable_system import generate_timetable
from timetable.utils import load_data, save_timetable

def main():
    print("📅 Automated Timetable Scheduler - IIIT Dharwad (Procedural)")

    # Load input data
    courses = load_data("courses.json")
    faculty = load_data("faculty.json")
    rooms = load_data("rooms.json")

    # Generate timetable
    timetable = generate_timetable(courses, faculty, rooms)

    # Save results
    save_timetable(timetable, "output/timetable.txt", "output/timetable.csv")

    print("✅ Timetable generated successfully! Check 'output/' folder.")

if __name__ == "__main__":
    main()
