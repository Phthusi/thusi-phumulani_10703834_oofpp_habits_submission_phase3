from ..view.get_habit_view import GetHabitView
from unittest import TestCase
from unittest.mock import patch, MagicMock


class TestGetHabitView(TestCase):
    def setUp(self):
        self.view = GetHabitView()

    # -------------------------------------------------
    # BASIC INTERNAL METHODS
    # -------------------------------------------------

    def test_normalize_empty(self):
        self.view.search_results = ""
        self.assertEqual(self.view._normalize_results(), [])

    def test_normalize_tuple(self):
        self.view.search_results = (1,2,3)
        result = self.view._normalize_results()
        self.assertEqual(result, [(1,2,3)])

    def test_normalize_list(self):
        data = [(1,2,3)]
        self.view.search_results = data
        self.assertEqual(self.view._normalize_results(), data)


    # -------------------------------------------------
    # DISPLAY FUNCTIONS
    # -------------------------------------------------

    @patch("builtins.print")
    def test_display_results_no_data(self, mock_print):
        self.view.search_results = []
        self.view.display_results()
        self.assertTrue(mock_print.called)

    @patch("builtins.print")
    def test_content_display_results_no_data(self, mock_print):
        self.view.search_results = []
        self.view.content_display_results()
        mock_print.assert_called()


    # -------------------------------------------------
    # SEARCH FLOWS
    # -------------------------------------------------


    @patch("src.components.get_habit.view.get_habit_view.prompt_input_for_commands")
    def test_search_by_name_invalid(self, mock_input):
        mock_input.return_value = "ab"  # too short
        cmd, msg, success = self.view.search_by_name()
        self.assertFalse(success)


    @patch("builtins.print")
    @patch("src.components.get_habit.view.get_habit_view.prompt_input_for_commands")
    def test_search_by_name_valid(self, mock_prompt, mock_print):
        mock_prompt.return_value = "Read"

        self.view.search_habit.search_by_name = MagicMock(
            return_value=[(1,2,"Reading","2025","1h","DONE")]
        )

        cmd, msg, success = self.view.search_by_name()
        self.assertTrue(success)


    @patch("src.components.get_habit.view.get_habit_view.prompt_input_for_commands")
    def test_search_by_date_error(self, mock_prompt):
        mock_prompt.return_value = "bad-date"

        self.view.search_habit.search_by_date = MagicMock(
            return_value=("error", "Invalid")
        )

        cmd, msg, success = self.view.search_by_date()
        self.assertFalse(success)


    @patch("builtins.print")
    @patch("src.components.get_habit.view.get_habit_view.prompt_input_for_commands")
    def test_search_by_status_valid(self, mock_prompt, mock_print):
        mock_prompt.return_value = "DONE"

        self.view.search_habit.search_by_status = MagicMock(
            return_value=[(1,2,"X","Y","Z","DONE")]
        )

        cmd, msg, success = self.view.search_by_status()
        self.assertTrue(success)


    # -------------------------------------------------
    # VIEW HABIT INFO
    # -------------------------------------------------

    @patch("builtins.print")
    @patch("src.components.get_habit.view.get_habit_view.prompt_input_for_commands")
    def test_view_habit_info_success(self, mock_prompt, mock_print):
        mock_prompt.return_value = "1"

        self.view.habit_factory.get_habit = MagicMock(
            return_value=(0,1,"Gym","2025","1h","UPCOMING","desc","refl")
        )

        cmd, msg, success = self.view.view_habit_information()
        self.assertTrue(success)


    @patch("src.components.get_habit.view.get_habit_view.prompt_input_for_commands")
    def test_view_habit_info_invalid_id(self, mock_prompt):
        mock_prompt.return_value = "abc"
        cmd, msg, success = self.view.view_habit_information()
        self.assertFalse(success)
