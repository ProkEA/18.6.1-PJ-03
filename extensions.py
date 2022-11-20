import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Ошибка! Невозможно перевести две одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Ошибка! Не удалось обработать запрос {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionException(f'Ошибка! Не удалось обработать запрос {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Ошибка! Не удалось обработать количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = amount * json.loads(r.content)[keys[base]]

        return total_base


class DeclensionByCases:
    def __init__(self, word, num):
        self.word = word
        self.num = num

    def incline(self):
        if self.word in ['Рубль', 'рубль', 'Рубли', 'рубли']:
            return'руб.'
        if self.word in ['Евро', 'евро']:
            return 'евро'
        if self.word in ['Доллар', 'доллар', 'Доллары', 'доллары']:
            return 'долл.'
