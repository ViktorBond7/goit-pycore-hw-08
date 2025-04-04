from input_error import input_error
from classes import AddressBook, Record
from parse_input import parse_input
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

@input_error   
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone= args
    print("name", name)
    print("old_phone", old_phone)
    print("new_phone", new_phone)
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        return f'Error: Contact {name} not found'

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return f"{'; '.join(phone.value for phone in record.phones)}"
    else:
        return f'Error: Contact {name} not found'

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts available."
    else:
        result = "\n".join(str(record) for record in book.data.values())
        return result

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        return "Неправильна кількість аргументів. Використовуйте: add-birthday [ім'я] [дата народження]"
    name, birthday = args
    record = book.find(name)
    if record:
        try:
            record.add_birthday(birthday)
            return f"День народження для {name} додано."
        except ValueError as e:
            return str(e)
    else:
        return f"Помилка: Контакт {name} не знайдено."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return f"День народження {record.birthday}"
    else:
        return f"Контакту з таким іменем не знайдено"

@input_error
def birthdays(book: AddressBook):
    birthdays = book.get_upcoming_birthdays()
    if birthdays:
        for birthday in birthdays:
            return f"{birthday['name']} - {birthday['congratulation_date']}"
    else:
        return "Відсутні дні народження на протязі 7 днів"


def main():
    book = load_data() 

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        match command:
            case "hello":
                print("How can I help you?")
            case "add":
                print(add_contact(args, book))
            case "change":
                print(change_contact(args, book))
            case "phone":
                print(show_phone(args, book))
            case "all":
                print(show_all(book))   
            case "add-birthday":
                print(add_birthday(args, book))
            case "show-birthday":
                print(show_birthday(args, book))
            case "birthdays":
                print(birthdays(book))
            case _:
                print("Invalid command.")

    save_data(book)  # Викликати перед виходом з програми

if __name__ == "__main__":
    main()

        




