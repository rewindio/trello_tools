from trello import TrelloClient, ResourceUnavailable
from helpers import *

class AddUserToBoards():
  def __init__(self, trello_client):
    self.trello_client = trello_client

  def run(self):
    self.__check_trello_auth()
    self.__workspace_selection()
  
  def __workspace_selection(self):
    self.workspace = None
    self.boards = None

    self.__choose_workspace()
    self.__load_boards()
    self.__add_user_to_boards()
  
  def __check_trello_auth(self):
    self.user = self.trello_client.get_member('me')
    confirmation = prompt_y_n(f"The user for this token is for \"{self.user.full_name} <{self.user.username}>\". Is this the correct user that you want added to the boards?")
    if not confirmation:
      print("Please create a new API key and token for the correct user. Exiting...")
      exit(1)

  def __choose_workspace(self):
    print("\nChoose a workspace to add the user to:")
    workspaces = self.trello_client.list_organizations()
    for idx, workspace in enumerate(workspaces):
      print(f"{idx+1}. {workspace.name}")
    print(f"{len(workspaces)+1}. Exit")
    choice = prompt_for_number(len(workspaces)+1)
    if choice == len(workspaces)+1:
      exit(0)

    self.workspace = workspaces[choice-1]
    print(f"\nWorkspace \"{self.workspace.name}\" selected.\n")

  def __load_boards(self):
    self.boards = self.workspace.all_boards()
    print(f"Found {len(self.boards)} boards in \"{self.workspace.name}\":")
    for idx, board in enumerate(self.boards):
      print(f"{idx+1}. {board.name}")

    resp = prompt_y_n(f"Would you like to add the user \"{self.user.full_name}\" to all of these boards?")
    if not resp:
      return self.__workspace_selection()

  def __add_user_to_boards(self):
    print("\nAdding user to boards...")
    for board in self.boards:
      self.__add_user_to_board(board)
    print("\nUser added to all boards!")
    resp = prompt_y_n("Would you like to the user to another workspace?")
    if resp:
      return self.__choose_workspace()
    else:
      print("Exiting...")
      exit(0)

  def __add_user_to_board(self, board):
    try:
      print(f"Adding user to \"{board.name}\"...", end="")
      board.add_member(self.user)
      print("Done!")
    except ResourceUnavailable as e:
      print(f"Failed to add user to board \"{board.name}\". Reason: {e}")
      if '429' in str(e):
        print("Rate limit exceeded. Waiting 10 seconds and trying again...")
        time.sleep(10)
        return self.__add_user_to_board(board)
      else:
        exit(1)
