import unittest
from unittest.mock import patch
from src import helpers

class HelpersTests(unittest.TestCase):

  @patch('builtins.input', return_value='')
  def test__press_enter_to_continue__waits_for_enter(self, mock_input):
    helpers.press_enter_to_continue()
    mock_input.assert_called_once_with('\nPress Enter to continue...')

  @patch('builtins.input', return_value='y')
  def test__prompt_y_n__returns_true_for_y(self, mock_input):
    self.assertEqual(helpers.prompt_y_n('prompt'), True)

  @patch('builtins.input', return_value='Y')
  def test__prompt_y_n__returns_true_for_Y(self, mock_input):
    self.assertEqual(helpers.prompt_y_n('prompt'), True)

  @patch('builtins.input', return_value='n')
  def test__prompt_y_n__returns_false_for_n(self, mock_input):
    self.assertEqual(helpers.prompt_y_n('prompt'), False)

  @patch('builtins.input', return_value='N')
  def test__prompt_y_n__returns_false_for_N(self, mock_input):
    self.assertEqual(helpers.prompt_y_n('prompt'), False)

  @patch('builtins.input', side_effect=['blah', 'y'])
  def test__prompt_y_n__prompts_again_if_invalid_input(self, mock_input):
    self.assertEqual(helpers.prompt_y_n('prompt'), True)
    self.assertEqual(mock_input.call_count, 2)

  @patch('builtins.input', return_value='2')
  def test__prompt_for_number__returns_number_if_valid(self, mock_input):
    self.assertEqual(helpers.prompt_for_number(4), 2)

  @patch('builtins.input', side_effect=['0', '-1', '2'])
  def test__prompt_for_number__prompts_again_if_less_than_1(self, mock_input):
    self.assertEqual(helpers.prompt_for_number(4), 2)
    self.assertEqual(mock_input.call_count, 3)

  @patch('builtins.input', side_effect=['5', '2'])
  def test__prompt_for_number__prompts_again_if_greater_than_num_choices(self, mock_input):
    self.assertEqual(helpers.prompt_for_number(4), 2)
    self.assertEqual(mock_input.call_count, 2)
