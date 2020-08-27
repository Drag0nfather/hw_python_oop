import datetime as dt


class Calculator:
    def __init__(self, limit):

        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today() 
        return sum([rec.amount for rec in self.records if today == rec.date])

    def get_week_stats(self):
        today = dt.datetime.now().date()
        sevendaysago = today - dt.timedelta(days=7)
        self.week_count = sum([count.amount for count in self.records 
                              if sevendaysago <= count.date <= today])
        return self.week_count

    def get_day_limit(self):
        return self.limit - self.get_today_stats()


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        balance = self.get_day_limit()
        if balance > 0:
            return ("Сегодня можно съесть что-нибудь "
             f"ещё, но с общей калорийностью не более {balance} кКал")
        else:
            return "Хватит есть!"


class CashCalculator(Calculator): 
    money_dict = {"rub" : ["руб", 1],
                  "usd" : ["USD", 71.0],
                  "eur" : ["Euro", 82.0],
                 }      

    def _init_(self, x=82.0, y=71.0):
        self.EURO_RATE = x
        self.USD_RATE = y
    @property
    def EURO_RATE(self):
        return self.money_dict["eur"][1]
    @EURO_RATE.setter
    def EURO_RATE(self, value):
        self.money_dict["eur"][1] = value
    @property
    def USD_RATE(self):
        return self.money_dict["usd"][1]
    @USD_RATE.setter
    def USD_RATE(self, value):
        self.money_dict["usd"][1] = value     

    def get_currency(self, currency):
        return self.money_dict[currency][1]

    def get_today_cash_remained(self, currency="rub"):
        if not currency in self.money_dict.keys():
            return None
        namecurrency = self.money_dict[currency][0]
        cashlim = self.get_day_limit()
        if cashlim == 0.0:
            return "Денег нет, держись"
        cashlim = round(cashlim / self.get_currency(currency), 2)
        if cashlim > 0.0: 
            return f"На сегодня осталось {cashlim} {namecurrency}"

        cashlim = abs(cashlim)
        return f"Денег нет, держись: твой долг - {cashlim} {namecurrency}"


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
