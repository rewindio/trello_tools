from trello import TrelloClient

class AddUserToBoards():
  def __init__(self):
    pass

  def run(self):
    self.__disclaimer()
    self.__collect_user_credentials()
    self.trello_client = TrelloClient(api_key=self.api_key, token=self.api_token)
    self.__check_trello_auth()

  def __press_enter_to_continue(self):
    input("\nPress Enter to continue...")
    print("\n")

  def __prompt_y_n(self, prompt):
    resp = input(f"{prompt} (y/n): ").lower().strip()
    if resp == 'y':
      return True
    elif resp == 'n':
      return False
    else:
      print("Invalid input. Please try again.")
      self.__prompt_y_n(prompt)
  
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
    user = self.trello_client.get_member('me')
    confirmation = self.__prompt_y_n(f"The user for this token is for \"{user.full_name} <{user.username}>\". Is this the correct user that you want added to the boards?")
    if not confirmation:
      print("Please create a new API key and token for the correct user. Exiting...")
      exit(1)
