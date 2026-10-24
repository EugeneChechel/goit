from collections import UserDict


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
            raise ValueError("Ім'я є обов'язковим.")

        super().__init__(value)


class Phone(Field):
    """Номер телефону. Допустимий формат — рівно 10 цифр."""

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Номер телефону має містити рівно 10 цифр.")

        super().__init__(value)

    @staticmethod
    def validate(value) -> bool:
        return isinstance(value, str) and value.isdigit() and len(value) == 10


class Record:
    """Запис адресної книги: ім'я та список телефонів."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone: str) -> None:
        """Додає телефон до запису."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Видаляє телефон із запису."""
        phone_obj = self.find_phone(phone)

        if phone_obj is None:
            raise ValueError("Телефон не знайдено.")

        self.phones.remove(phone_obj)

    def edit_phone(self, old_phone: str, new_phone: str) -> None:
        """Замінює існуючий телефон новим."""
        phone_obj = self.find_phone(old_phone)

        if phone_obj is None:
            raise ValueError("Телефон не знайдено.")

        index = self.phones.index(phone_obj)
        self.phones[index] = Phone(new_phone)

    def find_phone(self, phone: str) -> Phone | None:
        """Повертає об'єкт Phone або None, якщо номера немає в записі."""
        for phone_obj in self.phones:
            if phone_obj.value == phone:
                return phone_obj

        return None

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    """Адресна книга: додавання, пошук і видалення записів за іменем."""

    def add_record(self, record: Record) -> None:
        """Додає запис до книги. Ключ — ім'я контакту."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record | None:
        """Повертає запис за іменем або None, якщо контакту немає."""
        return self.data.get(name)

    def delete(self, name: str) -> None:
        """Видаляє запис за іменем."""
        if name not in self.data:
            raise KeyError("Контакт не знайдено.")

        del self.data[name]


if __name__ == "__main__":
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")
