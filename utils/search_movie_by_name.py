import requests
from typing import Optional, List

from config_data import config

API_URL = 'https://api.kinopoisk.dev/v1.4/movie/search'
headers = {'X-API-KEY': config.RAPID_API_KEY}


def search_movie_by_name_a_genre(movie_name: str, genre: Optional[str]=None, limit: int=250) -> Optional[List[dict]]:
    try:
        response = requests.get(API_URL, headers=headers, params={'query': movie_name, 'limit': limit})

        if response.status_code == 200:
            data = response.json()
            if data:
                exact_movies = []

                for movie in data['docs']:
                    names = movie['name'].lower()

                    if movie_name.lower() == names:

                        if genre:
                            movie_genres = [genres['name'].lower() for genres in movie['genres']]
                            if genre.lower() in movie_genres:
                                exact_movies.append(movie)

                        else:
                            exact_movies.append(movie)

                return exact_movies
            return None

    except Exception as e:
        print(f'Ошибка при запросе к API: {str(e)}')
        return None