"""CLI персонального помічника: контакти, нотатки, збереження даних."""

from __future__ import annotations

from functools import wraps

from models import PersonalAssistant, Record
from storage import load_data, save_data


HELP_TEXT = """
Personal Assistant — commands

Contacts:
  add-contact <name> [phone]
  add-phone <name> <phone>
  add-email <name> <email>
  add-address <name> <address...>
  add-birthday <name> <DD.MM.YYYY>
  change-phone <name> <old> <new>
  change-email <name> <email>
  change-address <name> <address...>
  change-birthday <name> <DD.MM.YYYY>
  delete-contact <name>
  delete-phone <name> <phone>
  show-contact <name>
  search-contacts <query...>
  all-contacts
  birthdays <days>

Notes:
  add-note <text...>
  add-note-tags <id> <tag> [tag...]
  remove-note-tag <id> <tag>
  edit-note <id> <new text...>
  delete-note <id>
  show-note <id>
  search-notes <query...>
  search-notes-tag <tag>
  sort-notes-by-tag
  all-notes

Other:
  help
  hello
  close | exit
""".strip()


def input_error(func):
    """Повертає текст помилки замість аварійного завершення."""

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except KeyError as error:
            message = error.args[0] if error.args else "Not found."
            return str(message) if isinstance(message, str) else "Not found."
        except IndexError:
            return "Not enough arguments. Type 'help' for usage."

    return inner


def parse_input(user_input: str):
    parts = user_input.strip().split()
    if not parts:
        return ("",)
    command, *args = parts
    return command.lower(), *args


def _require_contact(assistant: PersonalAssistant, name: str) -> Record:
    record = assistant.contacts.find(name)
    if record is None:
        raise KeyError("Contact not found.")
    return record


def _parse_note_id(raw: str) -> int:
    try:
        return int(raw)
    except ValueError:
        raise ValueError("Note id must be an integer.")


# --- Contacts ---


@input_error
def add_contact(args, assistant: PersonalAssistant):
    if not args:
        raise ValueError("Give me name please.")

    name, *rest = args
    if assistant.contacts.find(name):
        raise ValueError("Contact already exists. Use add-phone / add-email / ...")

    record = Record(name)
    if rest:
        record.add_phone(rest[0])

    assistant.contacts.add_record(record)
    return "Contact added."


@input_error
def add_phone(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone, *_ = args
    _require_contact(assistant, name).add_phone(phone)
    return "Phone added."


@input_error
def add_email(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me name and email please.")
    name, email, *_ = args
    _require_contact(assistant, name).set_email(email)
    return "Email added."


@input_error
def add_address(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me name and address please.")
    name, *address_parts = args
    _require_contact(assistant, name).set_address(" ".join(address_parts))
    return "Address added."


@input_error
def add_birthday(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday, *_ = args
    _require_contact(assistant, name).set_birthday(birthday)
    return "Birthday added."


@input_error
def change_phone(args, assistant: PersonalAssistant):
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")
    name, old_phone, new_phone, *_ = args
    _require_contact(assistant, name).edit_phone(old_phone, new_phone)
    return "Phone updated."


@input_error
def change_email(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me name and email please.")
    name, email, *_ = args
    _require_contact(assistant, name).set_email(email)
    return "Email updated."


@input_error
def change_address(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me name and address please.")
    name, *address_parts = args
    _require_contact(assistant, name).set_address(" ".join(address_parts))
    return "Address updated."


@input_error
def change_birthday(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")
    name, birthday, *_ = args
    _require_contact(assistant, name).set_birthday(birthday)
    return "Birthday updated."


@input_error
def delete_contact(args, assistant: PersonalAssistant):
    if not args:
        raise IndexError
    assistant.contacts.delete(args[0])
    return "Contact deleted."


@input_error
def delete_phone(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")
    name, phone, *_ = args
    _require_contact(assistant, name).remove_phone(phone)
    return "Phone deleted."


@input_error
def show_contact(args, assistant: PersonalAssistant):
    if not args:
        raise IndexError
    return str(_require_contact(assistant, args[0]))


@input_error
def search_contacts(args, assistant: PersonalAssistant):
    if not args:
        raise ValueError("Give me a search query.")
    results = assistant.contacts.search(" ".join(args))
    if not results:
        return "No contacts found."
    return "\n\n".join(str(record) for record in results)


@input_error
def all_contacts(args, assistant: PersonalAssistant):
    if not assistant.contacts.data:
        return "No contacts found."
    return "\n\n".join(str(record) for record in assistant.contacts.data.values())


@input_error
def birthdays(args, assistant: PersonalAssistant):
    if not args:
        raise ValueError("Give me number of days please.")
    try:
        days = int(args[0])
    except ValueError:
        raise ValueError("Days must be an integer.")

    upcoming = assistant.contacts.get_upcoming_birthdays(days)
    if not upcoming:
        return "No upcoming birthdays."

    lines = [
        f"{item['name']}: birthday {item['birthday']}, "
        f"congratulate on {item['congratulation_date']} (in {item['in_days']} day(s))"
        for item in upcoming
    ]
    return "\n".join(lines)


# --- Notes ---


@input_error
def add_note(args, assistant: PersonalAssistant):
    if not args:
        raise ValueError("Give me note text please.")
    note = assistant.notes.add(" ".join(args))
    return f"Note added with id {note.id}."


@input_error
def add_note_tags(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me note id and at least one tag.")
    note_id = _parse_note_id(args[0])
    note = assistant.notes.find(note_id)
    if note is None:
        raise KeyError("Note not found.")
    for tag in args[1:]:
        note.add_tag(tag)
    return "Tags added."


@input_error
def remove_note_tag(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me note id and tag.")
    note_id = _parse_note_id(args[0])
    note = assistant.notes.find(note_id)
    if note is None:
        raise KeyError("Note not found.")
    note.remove_tag(args[1])
    return "Tag removed."


@input_error
def edit_note(args, assistant: PersonalAssistant):
    if len(args) < 2:
        raise ValueError("Give me note id and new text.")
    note_id = _parse_note_id(args[0])
    note = assistant.notes.find(note_id)
    if note is None:
        raise KeyError("Note not found.")
    note.edit_text(" ".join(args[1:]))
    return "Note updated."


@input_error
def delete_note(args, assistant: PersonalAssistant):
    if not args:
        raise IndexError
    note_id = _parse_note_id(args[0])
    assistant.notes.delete(note_id)
    return "Note deleted."


@input_error
def show_note(args, assistant: PersonalAssistant):
    if not args:
        raise IndexError
    note_id = _parse_note_id(args[0])
    note = assistant.notes.find(note_id)
    if note is None:
        raise KeyError("Note not found.")
    return str(note)


@input_error
def search_notes(args, assistant: PersonalAssistant):
    if not args:
        raise ValueError("Give me a search query.")
    results = assistant.notes.search(" ".join(args))
    if not results:
        return "No notes found."
    return "\n\n".join(str(note) for note in results)


@input_error
def search_notes_tag(args, assistant: PersonalAssistant):
    if not args:
        raise ValueError("Give me a tag.")
    results = assistant.notes.search_by_tag(args[0])
    if not results:
        return "No notes found."
    return "\n\n".join(str(note) for note in results)


@input_error
def sort_notes_by_tag(args, assistant: PersonalAssistant):
    notes = assistant.notes.sorted_by_tag()
    if not notes:
        return "No notes found."
    return "\n\n".join(str(note) for note in notes)


@input_error
def all_notes(args, assistant: PersonalAssistant):
    notes = assistant.notes.all()
    if not notes:
        return "No notes found."
    return "\n\n".join(str(note) for note in notes)


COMMANDS = {
    "add-contact": add_contact,
    "add-phone": add_phone,
    "add-email": add_email,
    "add-address": add_address,
    "add-birthday": add_birthday,
    "change-phone": change_phone,
    "change-email": change_email,
    "change-address": change_address,
    "change-birthday": change_birthday,
    "delete-contact": delete_contact,
    "delete-phone": delete_phone,
    "show-contact": show_contact,
    "search-contacts": search_contacts,
    "all-contacts": all_contacts,
    "birthdays": birthdays,
    "add-note": add_note,
    "add-note-tags": add_note_tags,
    "remove-note-tag": remove_note_tag,
    "edit-note": edit_note,
    "delete-note": delete_note,
    "show-note": show_note,
    "search-notes": search_notes,
    "search-notes-tag": search_notes_tag,
    "sort-notes-by-tag": sort_notes_by_tag,
    "all-notes": all_notes,
}


def main():
    assistant = load_data()
    print("Welcome to the Personal Assistant!")
    print("Type 'help' to see available commands.")

    try:
        while True:
            try:
                user_input = input("Enter a command: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGood bye!")
                break

            command, *args = parse_input(user_input)

            if not command:
                print("Enter a command or type 'help'.")
            elif command in ("close", "exit"):
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "help":
                print(HELP_TEXT)
            elif command in COMMANDS:
                print(COMMANDS[command](args, assistant))
            else:
                print("Invalid command. Type 'help' for the list.")
    finally:
        save_data(assistant)


if __name__ == "__main__":
    main()
