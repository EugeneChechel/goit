import sys
from pathlib import Path

from colorama import Fore, Style, init


def print_directory_tree(path, indent=""):
    """
    Рекурсивно виводить структуру директорії.

    Args:
        path (Path): Шлях до директорії.
        indent (str): Відступ для вкладених елементів.
    """
    try:
        items = sorted(path.iterdir(), key=lambda item: (item.is_file(), item.name.lower()))

        for item in items:
            if item.is_dir():
                print(f"{indent}{Fore.BLUE}{item.name}/{Style.RESET_ALL}")
                print_directory_tree(item, indent + "    ")
            else:
                print(f"{indent}{Fore.GREEN}{item.name}{Style.RESET_ALL}")

    except PermissionError:
        print(f"{indent}{Fore.RED}Немає доступу до директорії: {path}{Style.RESET_ALL}")


def main():
    """
    Отримує шлях з аргументів командного рядка та запускає виведення дерева директорії.
    """
    init(autoreset=True)

    if len(sys.argv) != 2:
        print(f"{Fore.RED}Помилка: потрібно передати шлях до директорії.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Приклад: python colorama.py /шлях/до/директорії{Style.RESET_ALL}")
        return

    directory_path = Path(sys.argv[1])

    if not directory_path.exists():
        print(f"{Fore.RED}Помилка: шлях не існує: {directory_path}{Style.RESET_ALL}")
        return

    if not directory_path.is_dir():
        print(f"{Fore.RED}Помилка: вказаний шлях не є директорією: {directory_path}{Style.RESET_ALL}")
        return

    print(f"{Fore.BLUE}{directory_path.name}/{Style.RESET_ALL}")
    print_directory_tree(directory_path)


if __name__ == "__main__":
    main()