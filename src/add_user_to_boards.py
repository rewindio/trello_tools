from trello import TrelloClient

class AddUserToBoards():
  def __init__(self):
    pass

  def run(self):
    self.__disclaimer()
    self.__collect_user_credentials()
    self.trello_client = TrelloClient(api_key=self.api_key, token=self.api_token)
    self.__check_trello_auth()
    self.__workspace_selection()
  
  def __workspace_selection(self):
    self.workspace = None
    self.boards = None

    self.__choose_workspace()
    self.__load_boards()

  def __press_enter_to_continue(self):
    input("\nPress Enter to continue...")
    print("\n")

  def __prompt_y_n(self, prompt):
    resp = input(f"\n{prompt} (y/n): ").lower().strip()
    if resp == 'y':
      return True
    elif resp == 'n':
      return False
    else:
      print("Invalid input. Please try again.")
      return self.__prompt_y_n(prompt)
  
  def __prompt_for_number(self, num_choices):
    resp = input(f"\nEnter your choice: ")
    num = int(resp.strip())
    if num < 1 or num > num_choices:
      print("Invalid input. Please try again.")
      return self.__prompt_for_number(num_choices)
    return num
  
  def __disclaimer(self):
    print("""
This program will walk you through the process of adding your Trello user to the boards you have access to across any of your workspaces.

THIS WORK IS PROVIDED "AS IS," AND COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE OR DOCUMENT WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.

COPYRIGHT HOLDERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF ANY USE OF THE SOFTWARE OR DOCUMENT.""")

    self.__press_enter_to_continue()
  
  def __collect_user_credentials(self):
    print("""First, you'll need a Trello API key. This can be created here: https://id.atlassian.com/manage-profile/security/api-tokens

Make sure you are logged in with the correct user when you create the API key. Once created, copy the key to your clipboard. You'll need it in the next step.""")
    self.__press_enter_to_continue()

    self.api_key = input("Paste your API key here: ")
    self.api_token = input("Paste your API token here: ")

    if not self.api_key or not self.api_token:
      print("You must provide both an API key and token. Exiting...")
      exit(1)

  def __check_trello_auth(self):
    self.user = self.trello_client.get_member('me')
    confirmation = self.__prompt_y_n(f"The user for this token is for \"{self.user.full_name} <{self.user.username}>\". Is this the correct user that you want added to the boards?")
    if not confirmation:
      print("Please create a new API key and token for the correct user. Exiting...")
      exit(1)

  def __choose_workspace(self):
    print("\nChoose a workspace to add the user to:")
    workspaces = self.trello_client.list_organizations()
    for idx, workspace in enumerate(workspaces):
      print(f"{idx+1}. {workspace.name}")
    print(f"{len(workspaces)+1}. Exit")
    choice = self.__prompt_for_number(len(workspaces)+1)
    if choice == len(workspaces)+1:
      exit(0)

    self.workspace = workspaces[choice-1]
    print(f"\nWorkspace \"{self.workspace.name}\" selected.\n")

  def __load_boards(self):
    self.boards = self.workspace.all_boards()
    print(f"Found {len(self.boards)} boards in \"{self.workspace.name}\":")
    for idx, board in enumerate(self.boards):
      print(f"{idx+1}. {board.name}")

    resp = self.__prompt_y_n(f"Would you like to add the user \"{self.user.full_name}\" to all of these boards?")
    if not resp:
      return self.__workspace_selection()
