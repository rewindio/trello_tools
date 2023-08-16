from .add_user_to_boards import AddUserToBoards
from .helpers import press_enter_to_continue
from trello import TrelloClient
import argparse
import os

def main():
  parser = argparse.ArgumentParser(description='Blah blah')
  parser.add_argument('tool_name',
                      help='the name of the tool you want to run',
                      choices=['add-user-to-boards'])

  args = parser.parse_args()

  _disclaimer()
  api_key, api_token = _collect_user_credentials()
  trello_client = TrelloClient(api_key=api_key, token=api_token)

  if args.tool_name == 'add-user-to-boards':
    AddUserToBoards(trello_client).run()


def _disclaimer():
  # ruff: noqa: E501
  print("""
This software is provided by Rewind to help you manage your Trello account. It is not officially supported by Trello and Rewind is not responsible for any damage caused by the use of this software.

THIS WORK IS PROVIDED "AS IS," AND COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE OR DOCUMENT WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.

COPYRIGHT HOLDERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF ANY USE OF THE SOFTWARE OR DOCUMENT.""")

  press_enter_to_continue()

def _collect_user_credentials():
  api_key_env = os.environ.get('TRELLO_API_KEY')
  api_token_env = os.environ.get('TRELLO_API_TOKEN')
  if api_key_env and api_token_env:
    return [api_key_env, api_token_env]

  print("""First, you'll need a Trello API key. This can be created here: https://trello.com/power-ups/admin 

Make sure you are logged in with the correct user when you create the API key. Once created, copy the key to your clipboard. You'll need it in the next step.

See the README for more details.""")
  press_enter_to_continue()

  api_key = input("Paste your API key here: ")
  api_token = input("Paste your API token here: ")

  if not api_key or not api_token:
    print("You must provide both an API key and token. Exiting...")
    exit(1)

  return [api_key, api_token]
