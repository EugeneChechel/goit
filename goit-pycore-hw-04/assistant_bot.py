def parse_input(user_input):
    """
    Розбирає введений користувачем рядок на команду та аргументи.

    Args:
        user_input (str): Рядок, введений користувачем.

    Returns:
        tuple: Команда та список аргументів.
    """
    parts = user_input.strip().split()

    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


def add_contact(args, contacts):
    """
    Додає новий контакт до словника контактів.

    Args:
        args (list): Список з іменем та номером телефону.
        contacts (dict): Словник контактів.

    Returns:
        str: Повідомлення про результат виконання команди.
    """
    if len(args) != 2:
        return "Invalid command."

    name, phone = args
    contacts[name] = phone

    return "Contact added."


def change_contact(args, contacts):
    """
    Змінює номер телефону для існуючого контакту.

    Args:
        args (list): Список з іменем та новим номером телефону.
        contacts (dict): Словник контактів.

    Returns:
        str: Повідомлення про результат виконання команди.
    """
    if len(args) != 2:
        return "Invalid command."

    name, phone = args

    if name not in contacts:
        return "Contact not found."

    contacts[name] = phone

    return "Contact updated."


def show_phone(args, contacts):
    """
    Повертає номер телефону контакту за іменем.

    Args:
        args (list): Список з іменем контакту.
        contacts (dict): Словник контактів.

    Returns:
        str: Номер телефону або повідомлення про помилку.
    """
    if len(args) != 1:
        return "Invalid command."

    name = args[0]

    if name not in contacts:
        return "Contact not found."

    return contacts[name]


def show_all(contacts):
    """
    Повертає всі збережені контакти.

    Args:
        contacts (dict): Словник контактів.

    Returns:
        str: Усі контакти або повідомлення, що контактів немає.
    """
    if not contacts:
        return "No contacts found."

    result = []

    for name, phone in contacts.items():
        result.append(f"{name}: {phone}")

    return "\n".join(result)


def main():
    """
    Основний цикл роботи консольного бота-помічника.
    """
    contacts = {}

    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, contacts))

        elif command == "change":
            print(change_contact(args, contacts))

        elif command == "phone":
            print(show_phone(args, contacts))

        elif command == "all":
            print(show_all(contacts))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()