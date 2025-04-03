from functools import wraps

def validate_phone_number(func):
    """Декоратор для перевірки, що номер містить рівно 10 цифр."""
    @wraps(func)
    def wrapper(self, *args):
        # Визначаємо, який аргумент потрібно перевіряти
        if len(args) > 0:
            phone_number = args[-1]  # Завжди перевіряємо останній аргумент (new_phone або value)
            if not (phone_number.isdigit() and len(phone_number) == 10):
                raise ValueError("Phone number must be exactly 10 digits.")

        return func(self, *args)  # Викликаємо оригінальну функцію
    return wrapper

if __name__ == "__main__":
    validate_phone_number()