import requests
from typing import Optional, List

from config_data import config

API_URL = 'https://api.kinopoisk.dev/v1.4/movie'
headers = {'X-API-KEY': config.RAPID_API_KEY}

type_of_picture = {
    'фильм': 'movie',
    'сериал': 'tv-series',
    'аниме': 'anime',
    'мультфильм': 'cartoon',
    'анимационный сериал': 'animated-series'
}


def search_movie_by_rating(picture_type: str, kp_rating: str, limit: int=250) -> Optional[List[dict]]:
    valid_type = type_of_picture[picture_type.lower()]

    try:
        response = requests.get(
            url=API_URL,
            headers=headers,
            params={'type': valid_type, 'rating.kp': str(kp_rating), 'limit': limit}
        )

        if response.status_code == 200:
            data = response.json()
            if data:
                return data['docs']
            else:
                return None
    except Exception as e:
        print(f"Ошибка при запросе к API: {str(e)}")
        return None
