# GoIT — Artificial Intelligence and Machine Learning

Python exercises for the **Master of Science: Artificial Intelligence and Machine Learning** course from [GoIT](https://goit.global/).

Each homework is a small, self-contained script. The early assignments practice the language itself — dates, randomness, strings, and functions — before later work moves into data analysis and machine learning.

## Requirements

- Python 3.10 or newer
- No third-party packages. The exercises use only the standard library (`datetime`, `random`, `re`)

## Layout

Homework is grouped by GoIT module. A directory name follows the assignment id: `goit-<module>-hw-<number>`.

```text
goit-pycore-hw-03/    Python Core, homework 3
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
