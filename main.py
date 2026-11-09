from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must not be empty.")
        super().__init__(value.strip())


class Phone(Field):
    def __init__(self, value):
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]{10}", value):
            raise ValueError("Phone must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        value = Phone(phone)
        if self.find_phone(phone) is None:
            self.phones.append(value)

    def remove_phone(self, phone):
        found = self.find_phone(phone)
        if found is None:
            raise ValueError("Phone not found.")
        self.phones.remove(found)

    def edit_phone(self, old_phone, new_phone):
        replacement = Phone(new_phone)
        found = self.find_phone(old_phone)
        if found is None:
            raise ValueError("Phone not found.")
        duplicate = self.find_phone(new_phone)
        if duplicate is not None and duplicate is not found:
            raise ValueError("This phone already exists.")
        self.phones[self.phones.index(found)] = replacement

    def find_phone(self, phone):
        for item in self.phones:
            if item.value == phone:
                return item
        return None

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        del self.data[name]

    def __str__(self):
        rows = (str(record) for record in self.data.values())
        return "\n".join(rows) or "No contacts."


def main():
    book = AddressBook()
    john = Record("John")
    john.add_phone("1234567890")
    john.add_phone("5555555555")
    book.add_record(john)
    jane = Record("Jane")
    jane.add_phone("9876543210")
    book.add_record(jane)
    print(book)
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print(john)
    print(f"{john.name}: {john.find_phone('5555555555')}")
    book.delete("Jane")
    print(book)


if __name__ == "__main__":
    raise SystemExit(main())
