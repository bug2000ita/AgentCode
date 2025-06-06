# Terminal Games

This project contains simple terminal games written in Python.

## Installation

The Doom demo now uses pygame. Install dependencies with pip. Windows
users additionally need the `windows-curses` package:

```bash
pip install -r requirements.txt
```

## Running

Use `menu.py` to choose which program to run:

```bash
python menu.py
```

You can pick between the classic Snake game, a minimal Doom-like
first-person demo, or a simple Jira chatbot. The chatbot uses the MCP
server to query Jira issues. On first run it asks for your Jira URL,
username and API token and saves them in `jira_config.json`. In the Doom
demo press the space bar to shoot water from your pistol. A baby bear
enemy roams the map—if you bump into it, the demo ends. Press `q` to
exit a running game.
