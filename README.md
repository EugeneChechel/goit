# GoIT — Artificial Intelligence and Machine Learning

Python exercises for the **Master of Science: Artificial Intelligence and Machine Learning** course from [GoIT](https://goit.global/).

Each homework is a small, self-contained script. The assignments practice the language itself — functions, files, and command-line tools — before later work moves into data analysis and machine learning.

## Requirements

- Python 3.10 or newer
- Homework 3 uses only the standard library (`datetime`, `random`, `re`)
- Homework 4 uses the standard library (`pathlib`) plus [colorama](https://pypi.org/project/colorama/) for the directory tree:

```bash
pip install colorama
```

## Layout

Homework is grouped by GoIT module. A directory name follows the assignment id: `goit-<module>-hw-<number>`.

```text
goit-pycore-hw-03/    Python Core, homework 3
goit-pycore-hw-04/    Python Core, homework 4
```

Docstrings in the source are in Ukrainian, the language of the course.

## Python Core — Homework 3

Practice with dates, random sampling, and cleaning strings with regular expressions. Every file defines one function and a short example at the bottom, so running the file prints a sample result.

| Script | Function | What it does |
| --- | --- | --- |
| `get_days_from_today.py` | `get_days_from_today(date)` | Days between a `YYYY-MM-DD` date and today. A future date returns a negative number. An invalid date prints an error and returns `None`. |
| `get_numbers_ticket.py` | `get_numbers_ticket(min, max, quantity)` | A sorted list of unique random integers for a lottery ticket. `min` must be at least 1 and `max` at most 1000. Invalid arguments return an empty list. |
| `normalize_phone.py` | `normalize_phone(phone_number)` | A Ukrainian phone number rewritten for SMS: digits only, international form. A leading `+` is kept, `380…` becomes `+380…`, and a local number gets the `+38` prefix. |
| `get_upcoming_birthdays.py` | `get_upcoming_birthdays(users)` | Colleagues whose birthday falls within the next 7 days, including today. Birthdays use `YYYY.MM.DD`. A Saturday or Sunday birthday is congratulated on the following Monday. |

`get_days_from_today` and `get_upcoming_birthdays` use the current date, so their printed output changes from day to day. `get_numbers_ticket` draws a new sample on every run.

### Run

From the repository root:

```bash
python3 goit-pycore-hw-03/get_days_from_today.py
python3 goit-pycore-hw-03/get_numbers_ticket.py
python3 goit-pycore-hw-03/normalize_phone.py
python3 goit-pycore-hw-03/get_upcoming_birthdays.py
```

## Python Core — Homework 4

Practice with text files, recursion over a directory, and a small command-line assistant. Sample data lives in `goit-pycore-hw-04/files/`: `info` holds `name,salary` rows, and `cats` holds `id,name,age` rows.

| Script | Function | What it does |
| --- | --- | --- |
| `total_salary.py` | `total_salary(path)` | Reads a salary file and returns the total and the average. A missing file or a bad row prints an error and returns `(0, 0)`. |
| `get_cats_info.py` | `get_cats_info(path)` | Reads a cat file and returns a list of dictionaries with `id`, `name`, and `age`. A missing file or a bad row prints an error and returns an empty list. |
| `directory_tree.py` | `print_directory_tree(path)` | Prints a directory recursively. Directories are blue, files are green, and errors are red. Pass the directory path as the only command-line argument. |
| `assistant_bot.py` | `main()` | An in-memory contact bot. It keeps running until you exit. |

`total_salary.py` and `get_cats_info.py` open `./files/...`, so run them from inside `goit-pycore-hw-04`.

### Run

```bash
cd goit-pycore-hw-04
python3 total_salary.py
python3 get_cats_info.py
python3 directory_tree.py files
python3 assistant_bot.py
```

### Assistant commands

| Command | Effect |
| --- | --- |
| `hello` | Greeting |
| `add <name> <phone>` | Save a contact |
| `change <name> <phone>` | Replace a saved number |
| `phone <name>` | Print one number |
| `all` | Print every contact |
| `close` or `exit` | Quit |
