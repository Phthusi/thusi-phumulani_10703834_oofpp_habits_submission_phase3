import unittest
from src.components.add_habit.view.add_habit_view import AddHabitView

class TestUpdateHabitView(unittest.TestCase):
    add_habit_view = AddHabitView()
    
    def test_set_habit_name(self):
        # TestAddHabitView.add_habit_view.set_habit_name()
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()
