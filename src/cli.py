from add_user_to_boards import AddUserToBoards
import argparse

def main():
  parser = argparse.ArgumentParser(description='Blah blah')
  parser.add_argument('tool_name',
                      help='the name of the tool you want to run',
                      choices=['add-user-to-boards'])

  args = parser.parse_args()

  if args.tool_name == 'add-user-to-boards':
    AddUserToBoards().run()

if __name__ == "__main__":
  main()
