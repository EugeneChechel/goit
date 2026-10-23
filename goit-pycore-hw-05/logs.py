import sys
from pathlib import Path


def parse_log_line(line: str) -> dict:
    """
    Розбирає один рядок логу на складові частини:
    дата, час, рівень логування, повідомлення.
    """
    parts = line.strip().split(maxsplit=3)

    if len(parts) != 4:
        raise ValueError(f"Неправильний формат рядка логу: {line.strip()}")

    date, time, level, message = parts

    return {
        "date": date,
        "time": time,
        "level": level.upper(),
        "message": message,
    }


def load_logs(file_path: str) -> list:
    """
    Завантажує лог-файл і повертає список розібраних записів.
    """
    logs = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue

                try:
                    logs.append(parse_log_line(line))
                except ValueError as error:
                    print(f"Помилка в рядку {line_number}: {error}")

    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
    except PermissionError:
        print(f"Немає прав для читання файлу: {file_path}")
    except OSError as error:
        print(f"Помилка читання файлу: {error}")

    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """
    Фільтрує список логів за вказаним рівнем логування.
    """
    normalized_level = level.upper()

    return list(
        filter(
            lambda log: log["level"] == normalized_level,
            logs,
        )
    )


def count_logs_by_level(logs: list) -> dict:
    """
    Підраховує кількість записів для кожного рівня логування.
    """
    counts = {}

    for log in logs:
        level = log["level"]
        counts[level] = counts.get(level, 0) + 1

    return counts


def display_log_counts(counts: dict) -> None:
    """
    Виводить статистику логів у вигляді таблиці.
    """
    print("Рівень логування | Кількість")
    print("-----------------|----------")

    for level in ("INFO", "DEBUG", "ERROR", "WARNING"):
        print(f"{level:<16} | {counts.get(level, 0)}")


def display_log_details(logs: list, level: str) -> None:
    """
    Виводить детальну інформацію про записи певного рівня логування.
    """
    normalized_level = level.upper()

    print()
    print(f"Деталі логів для рівня '{normalized_level}':")

    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main() -> None:
    """
    Основна функція запуску скрипта.
    """
    if len(sys.argv) < 2:
        print("Використання: python main.py path/to/logfile.log [level]")
        return

    file_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) > 2 else None

    if not Path(file_path).is_file():
        print(f"Файл не знайдено: {file_path}")
        return

    logs = load_logs(file_path)

    if not logs:
        print("Логи відсутні або файл не містить коректних записів.")
        return

    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if level:
        filtered_logs = filter_logs_by_level(logs, level)

        if filtered_logs:
            display_log_details(filtered_logs, level)
        else:
            print()
            print(f"Записів рівня '{level.upper()}' не знайдено.")


if __name__ == "__main__":
    main()

# python3 logs.py logs