import pickle
from functools import wraps

from address_book import AddressBook, Phone, Record

FILENAME = "addressbook.pkl"


def save_data(book, filename=FILENAME):
    """Зберігає адресну книгу у файл через pickle."""
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename=FILENAME):
    """Завантажує адресну книгу. Якщо файлу немає — повертає порожню."""
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.

    Повідомлення ValueError повертається як є, щоб валідація телефону
    та дати народження лишалась зрозумілою.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."

    return inner


def parse_input(user_input: str):
    """Розбирає рядок на команду та аргументи."""
    parts = user_input.strip().split()

    if not parts:
        return ("",)

    command, *args = parts
    return command.lower(), *args


@input_error
def add_contact(args, book: AddressBook):
    """Додає новий контакт або ще один телефон до наявного."""
    if len(args) < 2:
        raise ValueError("Give me name and phone please.")

    name, phone, *_ = args
    Phone(phone)

    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    """Замінює один телефон контакту іншим."""
    if len(args) < 3:
        raise ValueError("Give me name, old phone and new phone please.")

    name, old_phone, new_phone, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    """Показує всі телефони контакту."""
    if not args:
        raise IndexError

    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError

    if not record.phones:
        return "No phones found."

    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(args, book: AddressBook):
    """Показує всі контакти адресної книги."""
    if not book.data:
        return "No contacts found."

    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    """Додає день народження контакту у форматі DD.MM.YYYY."""
    if len(args) < 2:
        raise ValueError("Give me name and birthday please.")

    name, birthday, *_ = args
    record = book.find(name)

    if record is None:
        raise KeyError

    message = "Birthday updated." if record.birthday else "Birthday added."
    record.add_birthday(birthday)
    return message


@input_error
def show_birthday(args, book: AddressBook):
    """Показує день народження контакту."""
    if not args:
        raise IndexError

    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError

    if record.birthday is None:
        return "Birthday not found."

    return str(record.birthday)


@input_error
def birthdays(args, book: AddressBook):
    """Показує привітання на найближчі 7 днів."""
    upcoming = book.get_upcoming_birthdays()

    if not upcoming:
        return "No upcoming birthdays."

    return "\n".join(
        f"{item['name']}: {item['congratulation_date']}"
        for item in upcoming
    )


def main():
    """Основний цикл. Книга читається на старті і записується перед виходом."""
    book = load_data()
    print("Welcome to the assistant bot!")

    try:
        while True:
            try:
                user_input = input("Enter a command: ")
            except (EOFError, KeyboardInterrupt):
                print("\nGood bye!")
                break

            command, *args = parse_input(user_input)

            if not command:
                print("Enter the argument for the command")
            elif command in ["close", "exit"]:
                print("Good bye!")
                break
            elif command == "hello":
                print("How can I help you?")
            elif command == "add":
                print(add_contact(args, book))
            elif command == "change":
                print(change_contact(args, book))
            elif command == "phone":
                print(show_phone(args, book))
            elif command == "all":
                print(show_all(args, book))
            elif command == "add-birthday":
                print(add_birthday(args, book))
            elif command == "show-birthday":
                print(show_birthday(args, book))
            elif command == "birthdays":
                print(birthdays(args, book))
            else:
                print("Invalid command.")
    finally:
        save_data(book)


if __name__ == "__main__":
    main()
