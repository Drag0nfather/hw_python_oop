import datetime as dt


class Calculator:
    def __init__(self, limit):

        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records += [record]

    def get_today_stats(self, date = None):
        if date is None:
            today = dt.datetime.now().date()
        else:
            if isinstance(date, str):
                today = dt.datetime.strptime(date, '%d.%m.%Y').date()
            else:
                today = date
        s = 0
        for r in self.records:
            if today == r.date:
                s += r.amount
        return s

    def get_week_stats(self):
        today = dt.datetime.now().date()
        s = 0
        for d in range(7):
            a = today - dt.timedelta(days=d)
            s += self.get_today_stats(a)
        return s
        

class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        a = self.limit - self.get_today_stats()
        if a > 0:
            return(f"Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {a} кКал")
        else:
            return("Хватит есть!")



class CashCalculator(Calculator):
    USD_RATE = 71.0
    EURO_RATE = 82.0

    def get_today_cash_remained(self, currency = "rub"):
        a = self.limit - self.get_today_stats()
        b = "руб"
        if currency == "usd":
            b = "USD"
            a = a / self.USD_RATE
        elif currency == "eur":
            b = "Euro"
            a = round(a / self.EURO_RATE, 2)
        if a > 0:
            return(f"На сегодня осталось {a} {b}")
        elif a == 0:
            return("Денег нет, держись")
        else:
            return(f"Денег нет, держись: твой долг - {-a} {b}")


class Record:
    def __init__(self, amount = 0, comment = "", date = None):
        self.amount = amount
        
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            if isinstance(date, str):
                self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
            else:
                self.date = date

        self.comment = comment



cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=145, comment="кофе")) 
cash_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
cash_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
print(cash_calculator.get_today_cash_remained("rub"))

calories_calculator = CaloriesCalculator(1000)
calories_calculator.add_record(Record(amount=145, comment="кофе")) 
calories_calculator.add_record(Record(amount=300, comment="Серёге за обед"))
calories_calculator.add_record(Record(amount=3000, comment="бар в Танин др", date="08.11.2019"))
print(calories_calculator.get_calories_remained())
