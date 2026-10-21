def total_salary(path):
    """
    Аналізує файл із зарплатами розробників і повертає
    загальну та середню суму заробітної плати.

    Args:
        path (str): Шлях до текстового файлу.

    Returns:
        tuple: Загальна сума зарплат і середня зарплата.
    """
    total = 0
    count = 0

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                name, salary = line.split(",")
                total += int(salary)
                count += 1

        average = total / count if count > 0 else 0

        return total, average

    except FileNotFoundError:
        print(f"Файл не знайдено: {path}")
        return 0, 0

    except ValueError:
        print("Файл містить некоректні дані.")
        return 0, 0

    except OSError:
        print("Помилка під час читання файлу.")
        return 0, 0


total, average = total_salary("./files/info")
print(f"Загальна сума заробітної плати: {total}, Середня заробітна плата: {average}")