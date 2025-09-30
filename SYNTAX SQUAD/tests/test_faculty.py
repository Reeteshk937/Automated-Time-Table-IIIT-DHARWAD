import unittest
from timetable.faculty import create_faculty
from timetable.room import create_room

class TestFacultyRoomFunctions(unittest.TestCase):
    def test_create_faculty(self):
        faculty = create_faculty("Dr. Hazra", "CSE", ["Mon", "Tue"])
        self.assertEqual(faculty["name"], "Dr. Hazra")
        self.assertIn("Mon", faculty["availability"])

    def test_create_room(self):
        room = create_room("A101", 60, "Lecture")
        self.assertEqual(room["room_number"], "A101")
        self.assertEqual(room["capacity"], 60)
        self.assertEqual(room["type"], "Lecture")

if __name__ == '__main__':
    unittest.main()
