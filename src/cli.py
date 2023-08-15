from .add_user_to_boards import AddUserToBoards
from .helpers import *
from trello import TrelloClient
import argparse

def main():
  parser = argparse.ArgumentParser(description='Blah blah')
  parser.add_argument('tool_name',
                      help='the name of the tool you want to run',
                      choices=['add-user-to-boards'])

  args = parser.parse_args()

  __disclaimer()
  api_key, api_token = __collect_user_credentials()
  trello_client = TrelloClient(api_key=api_key, token=api_token)

  if args.tool_name == 'add-user-to-boards':
    AddUserToBoards(trello_client).run()


def __disclaimer():
  print("""
This software is provided by Rewind to help you manage your Trello account. It is not officially supported by Trello and Rewind is not responsible for any damage caused by the use of this software.

THIS WORK IS PROVIDED "AS IS," AND COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE OR DOCUMENT WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.

COPYRIGHT HOLDERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF ANY USE OF THE SOFTWARE OR DOCUMENT.""")

  press_enter_to_continue()

def __collect_user_credentials():
  print("""First, you'll need a Trello API key. This can be created here: https://id.atlassian.com/manage-profile/security/api-tokens

Make sure you are logged in with the correct user when you create the API key. Once created, copy the key to your clipboard. You'll need it in the next step.

See the README for more details.""")
  press_enter_to_continue()

  api_key = input("Paste your API key here: ")
  api_token = input("Paste your API token here: ")

  if not api_key or not api_token:
    print("You must provide both an API key and token. Exiting...")
    exit(1)

  return [api_key, api_token]

if __name__ == "__main__":
  main()
