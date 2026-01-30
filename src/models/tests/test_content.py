import unittest
from src.models.content import HabitContent

class TestHabitContent(unittest.TestCase):

    def test_default_description_placeholder(self):
        c = HabitContent()
        self.assertEqual(c.get_description(), "nothing written yet")

    def test_set_description(self):
        c = HabitContent()
        c.set_description("Drink water")
        self.assertEqual(c.get_description(), "Drink water")

    def test_default_reflections_placeholder(self):
        c = HabitContent()
        self.assertEqual(c.get_reflections(), "nothing written yet")

    def test_set_reflections(self):
        c = HabitContent()
        c.set_reflections("Felt great today")
        self.assertEqual(c.get_reflections(), "Felt great today")

    def test_content_equality(self):
        c1 = HabitContent("Test")
        c2 = HabitContent("Test")
        self.assertEqual(c1, c2)

if __name__ == "__main__":
    unittest.main()
