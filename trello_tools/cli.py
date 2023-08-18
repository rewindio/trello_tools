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
NOT TECHNICAL ADVICE: Content made available on this page is intended solely for informational purposes only. It is not, and should not be taken, as professional technical advice by any user, who accepts full responsibility for its use. The content made available on this page is general in nature and without knowledge or reference to any users’ technical systems. No user should rely on, take or fail to take any action based on this content and, in all cases, should consult with their own technical advisors familiar with their technical systems before implementing any of the content made available here.

THE CONTENT ON THIS PAGE IS PROVIDED ON AN AS-IS BASIS WITH NO REPRESENTATIONS OF COMPLETENESS, ACCURACY, USEFULNESS OR TIMELINESS, AND WITHOUT WARRANTIES OF ANY KIND WHATSOEVER, EXPRESS OR IMPLIED.
""")

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
