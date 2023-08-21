# Trello Tools

> NOT TECHNICAL ADVICE: Content made available on this page is intended solely for informational purposes only. It is not, and should not be taken, as professional technical advice by any user, who accepts full responsibility for its use. The content made available on this page is general in nature and without knowledge or reference to any users’ technical systems. No user should rely on, take or fail to take any action based on this content and, in all cases, should consult with their own technical advisors familiar with their technical systems before implementing any of the content made available here.
>
> THE CONTENT ON THIS PAGE IS PROVIDED ON AN AS-IS BASIS WITH NO REPRESENTATIONS OF COMPLETENESS, ACCURACY, USEFULNESS OR TIMELINESS, AND WITHOUT WARRANTIES OF ANY KIND WHATSOEVER, EXPRESS OR IMPLIED.

This is a collection of scripts for interacting with your Trello account. Here are the available scripts:

- `add-user-to-boards` - Adds the authenticated user to all of the boards in the selected Trello workspace/organization. The user must already have access to the organization

# Usage

## Prerequisites

### 1. Trello Auth Token

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

### 2. Install Python and `pipenv`

Before you can run this, you need to have Python installed on your computer. Please find instructions for your OS to install:

- Windows: Install from the Microsoft store
- macOS: https://www.python.org/downloads/macos/ (or use `brew`)
- Linux: https://www.python.org/downloads/source/ (or use your distro's package manager)

Once Python has been installed, you will need to install `pipenv` to use this script. To do so, open your terminal (PowerShell if you're on Windows), and run this command:

```commandline
python3 -m pip install pipenv
```

After the installation is complete, run `python3 -m pipenv --version` to confirm it is working.

### 3. Download and run the script

1. Download this repository using a `git clone` or downloading the zip archive [here](https://github.com/rewindio/trello_tools/archive/refs/heads/main.zip)
2. If you downloaded the zip, extract it after it downloads
3. Open your terminal and navigate to the folder where the repository was cloned/extracted
    - If you're using Windows, you can navigate to the folder in Windows Explorer, then click on the address bar at the top and enter `powershell`, then hit Enter. This will open a terminal window in the correct directory
4. Run `python3 -m pipenv sync` to install the required dependencies
4. Run `python3 -m pipenv run trello_tools <tool_name>` in the terminal to start the script, where `<tool_name>` is one of the following:
    - `add-user-to-boards`

# Development

See https://packaging.python.org/en/latest/tutorials/managing-dependencies/

Install `pipenv`:

```commandline
python3 -m install --user pipenv
```

Install the dependencies:

```commandline
python3 -m pipenv sync
```

Running the CLI:

```commandline
python3 -m pipenv run trello_tools add-user-to-boards
```

Running the tests:

```commandline
python3 -m pipenv run test
```

Linting the code:

```commandline
python3 -m pipenv run lint
```
