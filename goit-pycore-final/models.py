"""Моделі контактів і нотаток для персонального помічника."""

from __future__ import annotations

import re
from collections import UserDict
from datetime import datetime, timedelta


class Field:
    """Базовий клас для полів запису."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Обов'язкове ім'я контакту."""

    def __init__(self, value):
        if not value or not str(value).strip():
            raise ValueError("Name is required.")

        super().__init__(str(value).strip())


class Phone(Field):
    """Номер телефону: рівно 10 цифр."""

    def __init__(self, value):
        value = str(value).strip()
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")

        super().__init__(value)


class Email(Field):
    """Електронна пошта з базовою валідацією формату."""

    PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    def __init__(self, value):
        value = str(value).strip()
        if not self.PATTERN.match(value):
            raise ValueError("Invalid email format.")

        super().__init__(value)


class Address(Field):
    """Адреса контакту. Може містити пробіли."""

    def __init__(self, value):
        value = str(value).strip()
        if not value:
            raise ValueError("Address cannot be empty.")

        super().__init__(value)


class Birthday(Field):
    """День народження у форматі DD.MM.YYYY."""

    def __init__(self, value):
        try:
            birthday = datetime.strptime(str(value).strip(), "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

        super().__init__(birthday)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Record:
    """Контакт: ім'я, телефони, email, адреса, день народження."""

    def __init__(self, name: str):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.email: Email | None = None
        self.address: Address | None = None
        self.birthday: Birthday | None = None

    def add_phone(self, phone: str) -> None:
        phone_obj = Phone(phone)
        if self.find_phone(phone_obj.value):
            raise ValueError("Phone already exists.")
        self.phones.append(phone_obj)

    def remove_phone(self, phone: str) -> None:
        phone_obj = self.find_phone(phone)
        if phone_obj is None:
            raise ValueError("Phone not found.")
        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        phone_obj = self.find_phone(old_phone)
        if phone_obj is None:
            raise ValueError("Phone not found.")

        new_phone_obj = Phone(new_phone)
        if old_phone != new_phone_obj.value and self.find_phone(new_phone_obj.value):
            raise ValueError("Phone already exists.")

        self.phones[self.phones.index(phone_obj)] = new_phone_obj

    def find_phone(self, phone: str) -> Phone | None:
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj
        return None

    def set_email(self, email: str) -> None:
        self.email = Email(email)

    def set_address(self, address: str) -> None:
        self.address = Address(address)

    def set_birthday(self, birthday: str) -> None:
        self.birthday = Birthday(birthday)

    def matches(self, query: str) -> bool:
        """Пошук за іменем, телефонами, email, адресою або днем народження."""
        query = query.lower()
        haystack = [
            self.name.value,
            str(self.email) if self.email else "",
            str(self.address) if self.address else "",
            str(self.birthday) if self.birthday else "",
            *[phone.value for phone in self.phones],
        ]
        return any(query in item.lower() for item in haystack if item)

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones) or "—"
        email = str(self.email) if self.email else "—"
        address = str(self.address) if self.address else "—"
        birthday = str(self.birthday) if self.birthday else "—"
        return (
            f"Contact: {self.name.value}\n"
            f"  phones: {phones}\n"
            f"  email: {email}\n"
            f"  address: {address}\n"
            f"  birthday: {birthday}"
        )


class AddressBook(UserDict):
    """Книга контактів."""

    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name not in self.data:
            raise KeyError("Contact not found.")
        del self.data[name]

    def search(self, query: str) -> list[Record]:
        query = query.strip()
        if not query:
            return []
        return [record for record in self.data.values() if record.matches(query)]

    def get_upcoming_birthdays(self, days: int) -> list[dict[str, str]]:
        """
        Контакти з днем народження протягом days днів, включно з сьогодні.
        Субота → понеділок, неділя → понеділок.
        """
        if days < 0:
            raise ValueError("Days must be a non-negative integer.")

        today = datetime.today().date()
        upcoming = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            birthday = record.birthday.value.date()
            birthday_this_year = self._birthday_in_year(birthday, today.year)

            if birthday_this_year < today:
                birthday_this_year = self._birthday_in_year(birthday, today.year + 1)

            days_until = (birthday_this_year - today).days
            if 0 <= days_until <= days:
                congratulation_date = birthday_this_year
                if congratulation_date.weekday() == 5:
                    congratulation_date += timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date += timedelta(days=1)

                upcoming.append(
                    {
                        "name": record.name.value,
                        "birthday": str(record.birthday),
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                        "in_days": str(days_until),
                    }
                )

        upcoming.sort(key=lambda item: int(item["in_days"]))
        return upcoming

    @staticmethod
    def _birthday_in_year(birthday, year):
        try:
            return birthday.replace(year=year)
        except ValueError:
            return birthday.replace(year=year, day=28)


class Note:
    """Нотатка з текстом і тегами."""

    def __init__(self, note_id: int, text: str, tags: list[str] | None = None):
        self.id = note_id
        self.text = text.strip()
        if not self.text:
            raise ValueError("Note text cannot be empty.")
        self.tags: list[str] = []
        for tag in tags or []:
            self.add_tag(tag)

    def add_tag(self, tag: str) -> None:
        normalized = tag.strip().lower().lstrip("#")
        if not normalized:
            raise ValueError("Tag cannot be empty.")
        if normalized not in self.tags:
            self.tags.append(normalized)

    def remove_tag(self, tag: str) -> None:
        normalized = tag.strip().lower().lstrip("#")
        if normalized not in self.tags:
            raise ValueError("Tag not found.")
        self.tags.remove(normalized)

    def edit_text(self, text: str) -> None:
        text = text.strip()
        if not text:
            raise ValueError("Note text cannot be empty.")
        self.text = text

    def matches(self, query: str) -> bool:
        query = query.lower()
        return query in self.text.lower() or any(query in tag for tag in self.tags)

    def has_tag(self, tag: str) -> bool:
        return tag.strip().lower().lstrip("#") in self.tags

    def __str__(self):
        tags = ", ".join(f"#{tag}" for tag in self.tags) or "—"
        return f"[{self.id}] {self.text}\n  tags: {tags}"


class Notebook:
    """Збірка нотаток з пошуком і сортуванням за тегами."""

    def __init__(self):
        self.notes: dict[int, Note] = {}
        self._next_id = 1

    def add(self, text: str, tags: list[str] | None = None) -> Note:
        note = Note(self._next_id, text, tags)
        self.notes[note.id] = note
        self._next_id += 1
        return note

    def find(self, note_id: int) -> Note | None:
        return self.notes.get(note_id)

    def delete(self, note_id: int) -> None:
        if note_id not in self.notes:
            raise KeyError("Note not found.")
        del self.notes[note_id]

    def search(self, query: str) -> list[Note]:
        query = query.strip()
        if not query:
            return []
        return [note for note in self.notes.values() if note.matches(query)]

    def search_by_tag(self, tag: str) -> list[Note]:
        return [note for note in self.notes.values() if note.has_tag(tag)]

    def sorted_by_tag(self) -> list[Note]:
        """Сортування: спочатку за першим тегом, потім за id."""
        return sorted(
            self.notes.values(),
            key=lambda note: (
                note.tags[0] if note.tags else "\uffff",
                note.id,
            ),
        )

    def all(self) -> list[Note]:
        return sorted(self.notes.values(), key=lambda note: note.id)


class PersonalAssistant:
    """Контейнер даних помічника: контакти + нотатки."""

    def __init__(self):
        self.contacts = AddressBook()
        self.notes = Notebook()
