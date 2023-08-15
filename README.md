# Usage

## Prerequisite

### Trello Auth Token

Before running this program, you will need to create a set of Trello credentials to be used. The credentials should be generated for the user that you want to add to the boards, so ensure you are logged in with that user when you complete these steps:

1. Go to Power-up Admin page: https://trello.com/power-ups/admin
1. Create a New Power-Up by clicking the "New" button in the top right of the Power-Up admin portal.
1. Fill out the following fields and click "Create":
  - Name (the first field) - this can be anything (i.e. "Rewind Trello Script")
  - Workspace - choose your personal workspace
  - Email - your email address
  - Support contact - your email address
  - Author - your name
1. On the next page, click "Generate a new API key"
1. Click "Generate API key" to confirm
1. Copy down the "API key" field - you'll need this later
1. Click on the "Token" hyperlink next to the API key field
1. You will be prompted to accept permission to access your account. Confirm the account shown is the one you want added to the boards, and click "Allow"
1. Copy down the token shown on the next screen - you'll need this later

# Development

See https://packaging.python.org/en/latest/tutorials/managing-dependencies/

Install `pipenv`:

```commandline
python3 -m pip install --user pipenv
```

Running the CLI:

```commandline
python3 -m pipenv run python -m src.cli add-user-to-boards
```

Running the tests:

```commandline
python3 -m pipenv run python -m unittest
```
