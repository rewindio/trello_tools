import unittest
import io
import sys

from trello_tools.add_user_to_boards import AddUserToBoards
from unittest.mock import MagicMock, patch, call
from trello import ResourceUnavailable

class AddUserToBoardsTests(unittest.TestCase):
  def setUp(self):
    self.mock_trello_client = MagicMock()
    self.test_class = AddUserToBoards(self.mock_trello_client)
  
  def build_mocks_with_names(self, names):
    # Name is a special key for MagicMock, so we need to do it in a 2-step process
    mocks = [MagicMock() for i in range(len(names))]
    [mocks[i].configure_mock(name=names[i]) for i in range(len(names))]
    return mocks

  @patch('trello_tools.helpers.get_input', return_value='y')
  def test__check_trello_auth__y(self, get_input_mock):
    self.mock_trello_client.get_member.return_value = MagicMock(full_name='Test Name', username='test_name')
    self.test_class._check_trello_auth()
    self.mock_trello_client.get_member.assert_called_with('me')
    get_input_mock.assert_called_with('\nThe user for this token is for "Test Name <test_name>". Is this the correct user that you want added to the boards? (y/n): ')

  @patch('trello_tools.helpers.get_input', return_value='n')
  @patch('builtins.print')
  def test__check_trello_auth__n(self, print_mock, get_input_mock):
    self.mock_trello_client.get_member.return_value = MagicMock(full_name='Test Name', username='test_name')
    with self.assertRaises(SystemExit):
      self.test_class._check_trello_auth()
      print_mock.assert_called_with('Please create a new API key and token for the correct user. Exiting...')

  @patch('trello_tools.helpers.get_input', return_value='1')
  @patch('builtins.print')
  def test__choose_workspace__lists_workspaces(self, print_mock, get_input_mock):
    mocks = self.build_mocks_with_names(['Workspace 1', 'Workspace 2', 'Workspace 3'])
    self.mock_trello_client.list_organizations.return_value = mocks
    self.test_class._choose_workspace()
    self.mock_trello_client.list_organizations.assert_called_with()
    print_mock.assert_has_calls([
      call('\nWorkspace "Workspace 1" selected.\n')
    ])

  @patch('trello_tools.helpers.get_input', return_value='4')
  def test__choose_workspace__lists_workspaces__exits(self, get_input_mock):
    mocks = self.build_mocks_with_names(['Workspace 1', 'Workspace 2', 'Workspace 3'])
    self.mock_trello_client.list_organizations.return_value = mocks
    with self.assertRaises(SystemExit):
      self.test_class._choose_workspace()
      self.mock_trello_client.list_organizations.assert_called_with()

  @patch('trello_tools.helpers.get_input', return_value='y')
  @patch('builtins.print')
  def test__load_boards__y(self, print_mock, get_input_mock):
    mocks = self.build_mocks_with_names(['Board 1', 'Board 2', 'Board 3'])
    self.test_class.user = MagicMock(full_name='Test Name', username='test_name')
    self.test_class.workspace = MagicMock()
    self.test_class.workspace.all_boards.return_value = mocks
    self.test_class._load_boards()
    self.test_class.workspace.all_boards.assert_called_with()
    print_mock.assert_has_calls([
      call('1. Board 1'),
      call('2. Board 2'),
      call('3. Board 3')
    ])
    get_input_mock.assert_called_with('\nWould you like to add the user "Test Name" to all of these boards? (y/n): ')

  @patch('trello_tools.helpers.get_input', return_value='n')
  def test__load_boards__n(self, get_input_mock):
    mocks = self.build_mocks_with_names(['Board 1', 'Board 2', 'Board 3'])
    self.test_class.user = MagicMock(full_name='Test Name', username='test_name')
    self.test_class.workspace = MagicMock()
    self.test_class.workspace.all_boards.return_value = mocks
    self.test_class._workspace_selection = MagicMock()
    self.test_class._load_boards()
    self.test_class.workspace.all_boards.assert_called_with()
    self.test_class._workspace_selection.assert_called_with()

  @patch('trello_tools.helpers.get_input', return_value='n')
  def test__add_user_to_boards__calls_add_user_to_board_for_each(self, get_input_mock):
    mocks = self.build_mocks_with_names(['Board 1', 'Board 2', 'Board 3'])
    self.test_class.boards = mocks
    self.test_class._add_user_to_board = MagicMock()
    with self.assertRaises(SystemExit):
      self.test_class._add_user_to_boards()
      self.test_class._add_user_to_board.assert_has_calls([
        call(mocks[0]),
        call(mocks[1]),
        call(mocks[2]),
      ])

  def test__add_user_to_board__calls_add_member(self):
    mock_board = MagicMock()
    self.test_class.user = MagicMock()
    self.test_class.user.configure_mock(name="Board 1")
    self.test_class._add_user_to_board(mock_board)
    mock_board.add_member.assert_called_with(self.test_class.user)

  @patch('time.sleep')
  def test__add_user_to_board__waits_and_retries_if_rate_limit_exceeded(self, sleep_mock):
    mock_board = MagicMock()
    mock_board.configure_mock(name="Board 1")
    self.test_class.user = MagicMock()
    mock_board.add_member.side_effect = [ResourceUnavailable('Rate limit exceeded', MagicMock(status_code=429)), None]
    self.test_class._add_user_to_board(mock_board)
    self.assertEqual(mock_board.add_member.call_count, 2)
    sleep_mock.assert_called_with(10)

  @patch('time.sleep')
  def test__add_user_to_board__exits_if_non_429_error(self, sleep_mock):
    mock_board = MagicMock()
    mock_board.configure_mock(name="Board 1")
    self.test_class.user = MagicMock()
    mock_board.add_member.side_effect = [ResourceUnavailable('Another error', MagicMock(status_code=500)), None]
    with self.assertRaises(SystemExit):
      self.test_class._add_user_to_board(mock_board)
      self.assertEqual(mock_board.add_member.call_count, 1)
      sleep_mock.assert_not_called()
