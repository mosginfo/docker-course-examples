from collections import defaultdict
from configparser import ConfigParser
import os
import sys
from textwrap import dedent

from weather import WeatherError, WeatherProviderFactory


def read_config_from_env(prefix_var: str = 'WEATHER_', default_section: str = 'main') -> dict[str, dict[str, str]]:
    config = defaultdict(dict)

    for name, value in os.environ.items():
        if name.startswith(prefix_var):
            pairs = name.replace(prefix_var, '', 1).lower().split('__')

            if len(pairs) == 1:
                section = default_section
                key = pairs[0]
            else:
                section, key = pairs

            config[section][key] = value

    return config


def main() -> int:
    if len(sys.argv) < 2:
        print('Positional argument "city" is required.', file=sys.stderr)
        sys.exit(1)

    config = ConfigParser()
    config.read('config.ini')
    config.read_dict(read_config_from_env())

    provider_name = config.get('main', 'provider_name', fallback='')

    if not config.has_section(provider_name):
        print(f'Unknown weather provider with name: "{provider_name}"', file=sys.stderr)
        return 1

    parameters = dict(config.items(provider_name))

    try:
        service = WeatherProviderFactory.create(provider_name, **parameters)

        city = sys.argv[1]
        info = service.get_weather(city)
        print(dedent(f'''
        Температура:   {info.temperature}° ({info.description})
        Ощущается как: {info.feels_like}°
        Ветер:         {info.wind} м/сек, {info.get_wind_direction()}
        Давление:      {info.pressure} мм рт. ст.
        Влажность:     {info.humidity}%
        '''))
        return 0
    except WeatherError as err:
        print(err, file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
