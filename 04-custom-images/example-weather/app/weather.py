from abc import ABC, abstractmethod
from dataclasses import dataclass
import typing as t

import requests


@dataclass
class WeatherInfo:
    temperature: float
    feels_like: float | None = None
    description: str = ''
    wind: float = -1
    wind_deg: int = -1
    pressure: float = -1
    humidity: int = -1

    def get_wind_direction(self) -> str:
        directions = (
            'С', 'ССВ', 'СВ', 'ВСВ', 'В', 'ВЮВ', 'ЮВ', 'ЮЮВ',
            'Ю', 'ЮЮЗ', 'ЮЗ', 'ЗЮЗ', 'З', 'ЗСЗ', 'СЗ', 'ССЗ',
        )
        index = round(self.wind_deg / 22.5) % 16
        return directions[index]


class WeatherError(Exception):
    pass


class WeatherProvider(ABC):
    @abstractmethod
    def get_weather(self, city: str) -> WeatherInfo:
        pass


class OpenWeatherMap(WeatherProvider):
    API_BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.api_key = api_key
    
    def get_weather(self, city: str) -> WeatherInfo:
        response = requests.get(self.API_BASE_URL, params={
            'appid': self.api_key,
            'q': city,
            'lang': 'ru',
            'units': 'metric',
        })
        data = response.json()

        if not response.ok:
            raise WeatherError(data['message'])

        description = [i['description'] for i in data['weather']]

        return WeatherInfo(
            temperature=data['main']['temp'],
            feels_like=data['main']['feels_like'],
            description=', '.join(description).capitalize(),
            wind=data['wind']['speed'],
            wind_deg=data['wind']['deg'],
            pressure=round(data['main']['pressure'] * 0.75),
            humidity=data['main']['humidity'],
        )


class WeatherAPI(WeatherProvider):
    API_BASE_URL = 'http://api.weatherapi.com/v1/current.json'

    def __init__(self, api_key: str) -> None:
        super().__init__()
        self.api_key = api_key
    
    def get_weather(self, city: str) -> WeatherInfo:
        response = requests.get(self.API_BASE_URL, params={
            'key': self.api_key,
            'q': city,
            'lang': 'ru',
        })
        data = response.json()

        if not response.ok:
            raise WeatherError(data['error']['message'])

        current = data['current']

        return WeatherInfo(
            temperature=current['temp_c'],
            feels_like=current['feelslike_c'],
            description=current['condition']['text'],
            wind=round(current['wind_kph'] / 3.6, 1),
            wind_deg=current['wind_degree'],
            pressure=round(current['pressure_mb'] * 0.75),
            humidity=current['humidity'],
        )


class WeatherProviderFactory:
    types = {
        'open_weather_map': OpenWeatherMap,
        'weather_api': WeatherAPI,
    }

    @classmethod
    def add_type(cls, name: str, klass: type[WeatherProvider]) -> None:
        if not name:
            raise WeatherError('Type must have a name.')

        if not issubclass(klass, WeatherProvider):
            raise WeatherError(f'Class "{klass}" is not WeatherProvider.')

        cls.types[name] = klass

    @classmethod
    def create(cls, name: str, *args: t.Any, **kwargs: t.Any) -> WeatherProvider:
        service_class = cls.types.get(name)

        if service_class is None:
            raise WeatherError(f'Weather provider with name "{name}" not found.')

        return service_class(*args, **kwargs)
