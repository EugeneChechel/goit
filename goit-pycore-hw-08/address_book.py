from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Обов'язкове поле з іменем контакту."""

    def __init__(self, value):
        if not value:
            raise ValueError("Name is required.")

        super().__init__(value)


class Phone(Field):
    """Номер телефону. Допустимий формат — рівно 10 цифр."""

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must contain exactly 10 digits.")

        super().__init__(value)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, str) and value.isdigit() and len(value) == 10


class Birthday(Field):
    """День народження у форматі DD.MM.YYYY. Зберігається як datetime."""

    def __init__(self, value):
        try:
            birthday = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Запис адресної книги: ім'я, список телефонів і один день народження."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str) -> None:
        """Додає телефон до запису."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Видаляє телефон із запису."""
        phone_obj = self.find_phone(phone)

        if phone_obj is None:
            raise ValueError("Phone not found.")

        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Замінює існуючий телефон новим."""
        phone_obj = self.find_phone(old_phone)

        if phone_obj is None:
            raise ValueError("Phone not found.")

        index = self.phones.index(phone_obj)
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        """Повертає об'єкт Phone або None, якщо номера немає в записі."""
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

        return None

    def add_birthday(self, birthday: str) -> None:
        """Додає або замінює єдиний день народження контакту."""
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones) or "no phones"
        birthday = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"


class AddressBook(UserDict):
    """Адресна книга: додавання, пошук, видалення і найближчі дні народження."""

    def add_record(self, record: Record) -> None:
        """Додає запис до книги. Ключ — ім'я контакту."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Повертає запис за іменем або None, якщо контакту немає."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за іменем."""
        if name not in self.data:
            raise KeyError("Contact not found.")

        del self.data[name]

    def get_upcoming_birthdays(self) -> list[dict[str, str]]:
        """
        Повертає контакти, яких потрібно привітати протягом 7 днів, включно з сьогодні.

        Якщо день народження припадає на суботу або неділю,
        дата привітання переноситься на наступний понеділок.
        """
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()
            birthday_this_year = self._birthday_in_year(birthday, today.year)

            if birthday_this_year < today:
                birthday_this_year = self._birthday_in_year(birthday, today.year + 1)

            days_until_birthday = (birthday_this_year - today).days

            if 0 <= days_until_birthday <= 7:
                congratulation_date = birthday_this_year

                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming_birthdays

    @staticmethod
    def _birthday_in_year(birthday, year):
        """29 лютого в невисокосний рік переносить на 28 лютого."""
        try:
            return birthday.replace(year=year)
        except ValueError:
            return birthday.replace(year=year, day=28)
