from datetime import datetime, timedelta


def get_upcoming_birthdays(users: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Повертає список користувачів, яких потрібно привітати з днем народження
    протягом найближчих 7 днів, включаючи поточний день.

    Якщо день народження припадає на суботу або неділю,
    дата привітання переноситься на наступний понеділок.

    Args:
        users (list[dict[str, str]]): Список словників з ключами:
            - name: ім'я користувача;
            - birthday: дата народження у форматі 'YYYY.MM.DD'.

    Returns:
        list[dict[str, str]]: Список словників з ключами:
            - name;
            - congratulation_date у форматі 'YYYY.MM.DD'.
    """
    today = datetime.today().date()
    upcoming_birthdays = []

    for user in users:
        try:
            birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()
        except ValueError:
            continue

        birthday_this_year = birthday.replace(year=today.year)

        if birthday_this_year < today:
            birthday_this_year = birthday_this_year.replace(year=today.year + 1)

        days_until_birthday = (birthday_this_year - today).days

        if 0 <= days_until_birthday <= 7:
            congratulation_date = birthday_this_year

            if congratulation_date.weekday() == 5:
                congratulation_date += timedelta(days=2)
            elif congratulation_date.weekday() == 6:
                congratulation_date += timedelta(days=1)

            upcoming_birthdays.append(
                {
                    "name": user["name"],
                    "congratulation_date": congratulation_date.strftime("%Y.%m.%d"),
                }
            )

    return upcoming_birthdays


users = [
    {"name": "John Doe", "birthday": "1985.01.23"},
    {"name": "Jane Smith", "birthday": "1990.10.19"},
]

upcoming_birthdays = get_upcoming_birthdays(users)

print("Список привітань на цьому тижні:", upcoming_birthdays)