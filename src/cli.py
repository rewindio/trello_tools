from add_user_to_boards import AddUserToBoards
from helpers import *
import argparse

def main():
  parser = argparse.ArgumentParser(description='Blah blah')
  parser.add_argument('tool_name',
                      help='the name of the tool you want to run',
                      choices=['add-user-to-boards'])

  args = parser.parse_args()

  if args.tool_name == 'add-user-to-boards':
    AddUserToBoards().run()

def __disclaimer():
  print("""
This software is provided by Rewind to help you manage your Trello account. It is not officially supported by Trello and Rewind is not responsible for any damage caused by the use of this software.

THIS WORK IS PROVIDED "AS IS," AND COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE OR DOCUMENT WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.

COPYRIGHT HOLDERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF ANY USE OF THE SOFTWARE OR DOCUMENT.""")

  press_enter_to_continue()

if __name__ == "__main__":
  __disclaimer()
  main()
