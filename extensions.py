import requests
import json

class APIException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message



class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f'https://api.exchangerate-api.com/v4/latest/{base}'
        response = requests.get(url)
        if response.status_code != 200:
            raise APIException('Ошибка при получении курса валют')
        response_data = response.json()
        if 'error' in response_data:
            raise APIException(response_data['error'])
        rate = response_data['rates'].get(quote)
        if rate is None:
            raise APIException(f'Не удалось получить курс {quote}')
        return rate * amount


class API:
    @staticmethod
    def get_price(base: str, quote: str, amount: float) -> float:
        url = f'https://api.exchangeratesapi.io/latest?base={base}&symbols={quote}'
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            raise APIException(data['error'])
        elif 'rates' not in data or quote not in data['rates']:
            raise APIException(f'Invalid currency: {quote}')
        else:
            rate = data['rates'][quote]
            return rate * amount
