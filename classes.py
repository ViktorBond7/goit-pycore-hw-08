from datetime import datetime, timedelta
from validate_phone import validate_phone_number
from input_error import input_error
from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    @validate_phone_number
    def __init__(self, value):
       super().__init__(value)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, number):
        self.phones.append(Phone(number))

    def remove_phone(self, number):
        self.phones = [phone for phone in self.phones if phone.value != number]
       
    @validate_phone_number
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return              
        raise ValueError(f"Phone number {old_phone} not found.")
    
    @input_error
    def find_phone(self, number):
        for phone in self.phones:
            if phone.value == number:
                return phone
        raise KeyError

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
  
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record #Додає запис до адресної книги

    def find(self, name):
        return self.data.get(name, None)      #Знаходить запис за ім'ям.

    def delete(self, name):                   #Видаляє запис за ім'ям.
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Record with name {name} not found.") 
 
    def show_birthday(self, name):
        record= self.data.get(name, None)
        if record and record.birthday:
            return f"День народження {name}: {record.birthday}"
        else:
            return f"Інформація про день народження для {name} відсутня."

    def get_upcoming_birthdays(self):
        result = []
        today = datetime.today().date()
        next_week = today + timedelta(days=7)

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday = record.birthday.value
            birthday_this_year = birthday.replace(year=today.year)
            
            # Якщо день народження вже минув цього року, переносимо його на наступний рік
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            # Якщо день народження випадає у наступний тиждень
            if today <= birthday_this_year <= next_week:
                weekday = birthday_this_year.weekday()
                if weekday == 6:
                    birthday_this_year += timedelta(days=1)
                elif weekday == 5:
                    birthday_this_year += timedelta(days=2)

                result.append({
                    "name": record.name.value,
                    "congratulation_date": birthday_this_year.strftime("%Y-%m-%d")
                })
        return result

class Birthday(Field):
    def __init__(self, value):
        try:
            # Перевіряємо формат і зберігаємо дату як datetime-об'єкт
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
# if __name__ == "__main__":
