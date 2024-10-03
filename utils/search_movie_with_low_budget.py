import requests
from typing import Optional, List
from config_data import config


type_of_picture = {
    'фильм': 'movie',
    'сериал': 'tv-series',
    'аниме': 'anime',
    'мультфильм': 'cartoon',
    'анимационный сериал': 'animated-series'
}


API_URL = 'https://api.kinopoisk.dev/v1.4/movie'
headers = {'X-API-KEY': config.RAPID_API_KEY}


def search_movie_by_low_budget(picture_type: str, curr: str) -> Optional[List[dict]]:
    valid_type = type_of_picture[picture_type.lower()]
    try:
        response = requests.get(
            url=API_URL,
            headers=headers,
            params={"type": valid_type, "selectFields": ["name", "description", "year", "rating",
                                                         "ratingMpaa", "genres", "poster", "budget"],
                    "notNullFields": ["name", "description", "year", "rating.kp",
                                      "ratingMpaa", "genres.name", "poster.url", "budget.value"], "limit": 250}
        )

        if response.status_code == 200:
            data = response.json()
            print('kkk')
            if data:
                print('jfj')
                new_l = []
                for movie in data['docs']:
                    if 'budget' in movie and 'value' in movie['budget'] and movie['budget']['currency'] == '$':
                        if movie['budget']['value'] <= int(curr):
                            new_l.append(movie)
                return new_l
            else:
                return None

    except Exception as e:
        print(f"Ошибка при запросе к API: {str(e)}")
        return None
