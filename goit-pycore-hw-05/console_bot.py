from functools import wraps


def input_error(func):
    """
    Декоратор для обробки помилок введення користувача.

    Обробляє винятки:
    - ValueError — неправильна кількість аргументів;
    - KeyError — контакт не знайдено;
    - IndexError — не передано потрібний аргумент.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name."

    return inner


def parse_input(user_input):
    """
    Розбирає введений користувачем рядок на команду та аргументи.
    """
    cmd, *args = user_input.strip().split()
    cmd = cmd.lower()

    return cmd, args


@input_error
def add_contact(args, contacts):
    """
    Додає новий контакт до словника контактів.
    """
    if len(args) != 2:
        raise ValueError

    name, phone = args
    contacts[name] = phone

    return "Contact added."


@input_error
def change_contact(args, contacts):
    """
    Змінює номер телефону для існуючого контакту.
    """
    if len(args) != 2:
        raise ValueError

    name, phone = args

    if name not in contacts:
        raise KeyError

    contacts[name] = phone

    return "Contact updated."


@input_error
def show_phone(args, contacts):
    """
    Показує номер телефону для вказаного контакту.
    """
    name = args[0]

    if name not in contacts:
        raise KeyError

    return contacts[name]


@input_error
def show_all(args, contacts):
    """
    Показує всі збережені контакти.
    """
    if not contacts:
        return "No contacts found."

    return "\n".join(
        f"{name}: {phone}"
        for name, phone in contacts.items()
    )


def main():
    """
    Основний цикл роботи консольного бота.
    """
    contacts = {}

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")

        if not user_input.strip():
            print("Enter the argument for the command")
            continue

        try:
            command, args = parse_input(user_input)
        except ValueError:
            print("Enter the argument for the command")
            continue

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(args, contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()