import unittest
import sys
import os

# Add the root directory (SYNTAX SQUAD) to sys.path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from timetable.timetable_system import generate_timetable

class TestTimetableSystem(unittest.TestCase):
    def test_generate_timetable(self):
        courses = [
            {"code": "CS261", "name": "Operating System", "credits": 2.0, "faculty": "Dr. Suvadip Hazra"}
        ]
        faculty = [
            {"name": "Dr. Suvadip Hazra", "department": "CSE", "availability": ["Mon", "Wed", "Fri"]}
        ]
        rooms = [
            {"room_number": "A101", "capacity": 60, "type": "Lecture"}
        ]

        timetable = generate_timetable(courses, faculty, rooms)

        self.assertEqual(len(timetable), 1)
        self.assertEqual(timetable[0]["faculty"], "Dr. Suvadip Hazra")
        self.assertEqual(timetable[0]["room"], "A101")

if __name__ == '__main__':
    unittest.main()
