import datetime as dt


class Calculator:
    def __init__(self, limit):

        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self, date=None):
        if date is None:
            today = dt.datetime.now().date()
        else:
            if isinstance(date, str):
                today = dt.datetime.strptime(date, '%d.%m.%Y').date()
            else:
                today = date
        return sum([rec.amount for rec in self.records if today == rec.date])

    def get_week_stats(self):
        today = dt.datetime.now().date()
        days_count = [today - dt.timedelta(days=day) for day in range(7)]
        return sum([self.get_today_stats(days_count[day]) \
            for day in range(7)])

    def get_day_limit(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balance = self.get_day_limit()
        if balance > 0:
            return(f"Сегодня можно съесть что-нибудь ещё, \
но с общей калорийностью не более {balance} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator):
    EURO_RATE = 82.0
    USD_RATE = 71.0
    def get_currency(self, currency):
        if currency == "usd":
            return self.USD_RATE
        if currency == "eur":
            return self.EURO_RATE
        return 1.0
    
    money_dict = {"rub" : "руб",
                  "usd" : "USD",
                  "eur" : "Euro"
                 }

    def get_today_cash_remained(self, currency="rub"):
        if currency not in self.money_dict.keys():
            return None
        b = self.money_dict[currency]
        a = round(self.get_day_limit() / self.get_currency(currency), 2)
        if a == 0.0: return "Денег нет, держись"
        if a > 0.0: 
            return f"На сегодня осталось {a} {b}"
        return f"Денег нет, держись: твой долг - {abs(a)} {b}"


class Record:
    def __init__(self, amount=0, comment="", date=None):
        self.amount = amount
        
        if date is None:
            self.date = dt.date.today()
        else:
            if isinstance(date, str):
                self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
            else:
                self.date = date

        self.comment = comment

if __name__ == "__main__":
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment="кофе")) 
    cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др",
    date="08.11.2019"))
    print(cash_calculator.get_today_cash_remained("rub"))

    calories_calculator = CaloriesCalculator(1000)
    calories_calculator.add_record(Record(amount=145, comment="кофе")) 
    calories_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
    calories_calculator.add_record(Record(amount=3000, comment="бар в Танин др",
    date="08.11.2019"))
    print(calories_calculator.get_calories_remained())
