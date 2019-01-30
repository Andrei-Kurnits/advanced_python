class Exchanger:
    _base = None

    @staticmethod
    def exchange(money, to_currency="USD"):
        ratio = Exchanger._base.get((money.currency, to_currency))
        if ratio is None:
            # print("{} to {} ratio hasn't found! Used 1.0 as the ratio.")
            ratio = 1.0
        return Money(money.amount * ratio, to_currency)


class ExchangerOnline(Exchanger):
    @staticmethod
    def exchange(money, to_currency="USD"):
        if Exchanger._base is None:  # if dictionary is empty
            data = ExchangerOnline.request_exchange_data()
            Exchanger._base = ExchangerOnline.parse_exchange_data(data)
        return Exchanger.exchange(money, to_currency)

    @staticmethod
    def request_exchange_data():
        import urllib.request
        import json
        access_key = "618af75c65d8fff43dda6794e6dee22e"
        content = urllib.request.urlopen("http://www.apilayer.net/api/live?access_key={}".format(access_key)).read()
        data = json.loads(content.decode('utf-8'))
        return data

    @staticmethod
    def parse_exchange_data(data):
        base = dict()
        for currencies, rate in data['quotes'].items():
            cur_from = currencies[0:3]
            cur_to = currencies[3:6]
            base.update({(cur_from, cur_to): rate})

        unique_currencies = set()
        unique_currencies.add("USD")
        for k, v in base:
            unique_currencies.add(v)
        unique_currencies = list(unique_currencies)
        print("Unique currencies:", len(unique_currencies))

        for c1 in unique_currencies:
            for c2 in unique_currencies:
                if base.get((c1, c2)) is None:
                    r1 = base.get(("USD", c1))
                    r2 = base.get(("USD", c2))
                    base.update({(c1, c2): r2 / r1})

        print("Exchange base records:", len(base))

        return base


class Money:

    _exchanger = ExchangerOnline

    def __init__(self, amount=0, currency="USD"):
        if isinstance(amount, Money):
            self.amount = amount.amount
            self.currency = amount.currency
        else:
            self.amount = amount
            self.currency = currency

    def __str__(self):
        return "{} {}".format(self.amount, self.currency)

    def __add__(self, another):
        money = Money(another)
        exchanged = Money._exchanger.exchange(money, self.currency)
        return Money(self.amount + exchanged.amount, self.currency)

    def __radd__(self, another):
        return self.__add__(another)

    def __mul__(self, mul):
        return Money(self.amount * mul, self.currency)

    def __rmul__(self, mul):
        return self.__mul__(mul)


if __name__ == "__main__":

    x = Money(10, "BYN")
    y = Money(11) # define your own default value, e.g. “USD”
    z = Money(12.34, "EUR")

    print(z + 3.11*x + y*0.8)  # result in “EUR”

    lst = [Money(10,"BYN"), Money(11), Money(12.01, "JPY")]
    s = sum(lst)
    print(s)  # result in “BYN”
