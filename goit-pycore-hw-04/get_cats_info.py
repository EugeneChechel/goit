def get_cats_info(path):
    """
    Читає файл з інформацією про котів і повертає список словників.

    Args:
        path (str): Шлях до текстового файлу.

    Returns:
        list: Список словників з інформацією про котів.
    """
    cats_info = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                cat_id, name, age = line.split(",")

                cats_info.append({
                    "id": cat_id,
                    "name": name,
                    "age": age,
                })

        return cats_info

    except FileNotFoundError:
        print(f"Файл не знайдено: {path}")
        return []

    except ValueError:
        print("Файл містить некоректні дані.")
        return []

    except OSError:
        print("Помилка під час читання файлу.")
        return []


cats_info = get_cats_info("./files/cats")
print(cats_info)