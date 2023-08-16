import time
from trello import ResourceUnavailable, Board as TrelloBoard
from .helpers import prompt_y_n, prompt_for_number

class AddUserToBoards():
  def __init__(self, trello_client):
    self.trello_client = trello_client

  def run(self):
    self._check_trello_auth()
    self._workspace_selection()
  
  def _workspace_selection(self):
    self.workspace = None
    self.boards = None

    self._choose_workspace()
    self._load_boards()
    self._add_user_to_boards()
  
  def _check_trello_auth(self):
    self.user = self.trello_client.get_member('me')
    confirmation = prompt_y_n(
      f"The user associated with this token is \"{self.user.full_name} " + 
      f"<{self.user.username}>\". Is this the correct user that you want " +
      "added to the boards?"
    )
    if not confirmation:
      print("Please create a new API key and token for the correct user. Exiting...")
      exit(1)

  def _choose_workspace(self):
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

  def _load_boards(self):
    all_boards = self._fetch_boards_for_workspace_with_memberships()
    self.boards = [board for board in all_boards if not board.user_is_member(self.user)]
    num_total_boards = len(all_boards)
    num_boards_to_add = len(self.boards)
    num_boards_joined = num_total_boards - num_boards_to_add

    print(f"Found {len(all_boards)} boards in \"{self.workspace.name}\".")
    print(f"{self.user.full_name} is already a member of {num_boards_joined} of these.")
    if len(self.boards) == 0:
      print("There are no boards to add the user to. Returning to workspace selection")
      return self._workspace_selection()
    print(f"Joining {len(self.boards)} boards:")
    for idx, board in enumerate(self.boards):
      print(f"{idx+1}. {board.name}")

    resp = prompt_y_n(
      f"Would you like to add the user \"{self.user.full_name}\" " +
      "to all of these boards?"
    )
    if not resp:
      return self._workspace_selection()

  def _add_user_to_boards(self):
    print("\nAdding user to boards...")
    for board in self.boards:
      self._add_user_to_board(board)
    print("\nUser added to all boards!")
    resp = prompt_y_n("Would you like to add the user to boards in another workspace?")
    if resp:
      return self._workspace_selection()
    else:
      print("Exiting...")
      exit(0)

  def _add_user_to_board(self, board):
    try:
      print(f"Adding user to \"{board.name}\"...", end="")
      board.add_member(self.user)
      print("Done!")
    except ResourceUnavailable as e:
      print(f"Failed to add user to board \"{board.name}\". Reason: {e}")
      if '429' in str(e):
        print("Rate limit exceeded. Waiting 10 seconds and trying again...")
        time.sleep(10)
        return self._add_user_to_board(board)
      else:
        exit(1)

  def _fetch_boards_for_workspace_with_memberships(self):
    url = f"/organizations/{self.workspace.id}/boards"
    json_obj = self.trello_client.fetch_json(url)
    return [
      Board.from_json(organization=self.workspace, json_obj=obj) for obj in json_obj
    ]


class Board(TrelloBoard):
  @classmethod
  def from_json(cls, trello_client=None, organization=None, json_obj=None):
    board = super(Board, cls).from_json(
      trello_client=trello_client, organization=organization, json_obj=json_obj
    )
    board = Board(client=board.client, board_id=board.id, organization=board.organization, name=board.name)
    board.memberships = json_obj['memberships']
    return board
  
  def user_is_member(self, user):
    return any([membership['idMember'] == user.id for membership in self.memberships])
