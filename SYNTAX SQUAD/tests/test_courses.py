import unittest
from timetable.course import create_course

class TestCourseFunctions(unittest.TestCase):
    def test_create_course(self):
        course = create_course("CS261", "Operating System", 2.0, "Dr. Hazra", 3)
        self.assertEqual(course["code"], "CS261")
        self.assertEqual(course["name"], "Operating System")
        self.assertEqual(course["credits"], 2.0)
        self.assertEqual(course["faculty"], "Dr. Hazra")
        self.assertEqual(course["semester"], 3)

if __name__ == '__main__':
    unittest.main()
