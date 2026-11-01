# Personal Assistant

CLI personal assistant for the GoIT Python Core final project: contacts, notes with tags, and persistent storage.

## Install

From this directory:

```bash
pip install .
```

For development (editable install):

```bash
pip install -e .
```

After installation the command `personal-assistant` is available from any directory.

## Run

```bash
personal-assistant
```

Or without installing:

```bash
python3 -m personal_assistant
```

Type `help` inside the bot for the full command list.

## Data

Contacts and notes are saved with `pickle` to:

```text
~/.personal_assistant/assistant.pkl
```

## Package layout

| Path | Role |
| --- | --- |
| `personal_assistant/models.py` | Fields, contacts, notes |
| `personal_assistant/storage.py` | Load and save in the home directory |
| `personal_assistant/assistant.py` | Command loop (`main` entry point) |
