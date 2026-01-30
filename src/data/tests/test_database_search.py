import unittest
import os

from src.data.database_interface import DatabaseInterface
from src.models.habit import Habit

class TestDatabaseSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary test database
        cls.test_db_name = "test_habit.db"
        cls.db = DatabaseInterface(cls.test_db_name)

        # Insert test data
        habit1 = Habit("Reading", "2025-03-10 10:00:00", "01:00:00")
        habit1.content.set_description("Read Python book")
        habit1.content.set_reflections("Good progress")
        habit1.set_status("DONE")
        cls.db.add_habit(habit1)

        habit2 = Habit("Gym", "2025-04-15 09:00:00", "02:00:00")
        habit2.content.set_description("Workout session")
        habit2.content.set_reflections("Leg day")
        habit2.set_status("UPCOMING")
        cls.db.add_habit(habit2)

    @classmethod
    def tearDownClass(cls):
        # Remove test database file after tests
        try:
            os.remove(cls.test_db_name)
        except:
            pass

    # ---- search_by_content ----
    def test_search_by_content(self):
        result = self.db.search_by_content("Python")
        self.assertTrue(len(result) >= 1)

    # ---- get_name_with_text ----
    def test_search_by_name(self):
        result = self.db.get_name_with_text("Gym")
        self.assertEqual(result[0][2], "Gym")

    # ---- search_by_month ----
    def test_search_by_month(self):
        status, result = self.db.search_by_month(3, 2025)
        self.assertEqual(status, "success")
        self.assertTrue(len(result) >= 1)

    # ---- search_by_date ----
    def test_search_by_date(self):
        status, result = self.db.search_by_date("2025-04-15")
        self.assertEqual(status, "success")
        self.assertTrue(len(result) >= 1)
        TestDatabaseSearch.tearDownClass()


if __name__ == "__main__":
    unittest.main()
    TestDatabaseSearch.tearDownClass()