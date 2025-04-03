from datetime import datetime, timedelta
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