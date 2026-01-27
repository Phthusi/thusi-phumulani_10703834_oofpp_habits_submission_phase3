import unittest
from unittest.mock import patch
from src.components.add_habit.view.add_habit_view import AddHabitView
class TestAddHabitView(unittest.TestCase):

    @patch('src.services.inputs.prompt_input_for_commands', return_value='ab')
    def test_invalid_name_prints_error(self, mock_input):
        view = AddHabitView()
        # call the original function directly, bypassing decorators
        command, message, success = view.set_habit_name.__wrapped__(view)
        self.assertFalse(success)
        self.assertEqual(message, "Name must have more than 2 characters")

    @patch('src.services.inputs.prompt_input_for_commands', return_value='MyHabit')
    def test_valid_name(self, mock_input):
        view = AddHabitView()
        command, message, success = view.set_habit_name.__wrapped__(view)
        self.assertTrue(success)
        self.assertEqual(view.get_habit_name(), "MyHabit")

        
if __name__ == '__main__':
    unittest.main()
