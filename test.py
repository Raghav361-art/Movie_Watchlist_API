import requests

class QueryMovie:
    GENRES = {
        28: "Action",
        12: "Adventure",
        16: "Animation",
        35: "Comedy",
        80: "Crime",
        99: "Documentary",
        18: "Drama",
        10751: "Family",
        14: "Fantasy",
        36: "History",
        27: "Horror",
        10402: "Music",
        9648: "Mystery",
        10749: "Romance",
        878: "Science Fiction",
        10770: "TV Movie",
        53: "Thriller",
        10752: "War",
        37: "Western"
    }

    def __init__(self, query):
        self.query = query



    def get_all(self):
        url_qu = f"https://api.themoviedb.org/3/search/movie?query={self.query}"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmNjdlN2NkM2I0ZmE3M2M5NWFjNDY4YzU5ZWMyODQ2ZSIsIm5iZiI6MTc4OTczNzM0Ny42NzEsInN1YiI6IjZhYWQzOTgzZTA1MDgwOGFiMTM1ZjVlMCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.glSxJTCM98AkavrABRSfSLg9Rg3pHy_ugB3muZh_7cc"
            }


        resp_qu = requests.get(url_qu, headers=headers, timeout=15)
        resp_qu.raise_for_status()
        data_qu = resp_qu.json()

        query_results = []

        for i in range(min(len(data_qu["results"]), 5)):
            query = data_qu["results"][i]
            id = query["id"]
            img_path = query["poster_path"]


            url = f"https://api.themoviedb.org/3/movie/{id}/credits?language=en-US"
            
            try:
                response = requests.get(url, headers=headers, timeout=15)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException:
                data = {"crew": []}

            title = query["title"]
            director = next((person["name"]for person in data["crew"] if person["job"] == "Director"), None)
            release_year = query["release_date"]
            rating = query["vote_average"]
            img_url = f"https://image.tmdb.org/t/p/w185/{img_path}" if img_path else None
            genres = ", ".join(
                self.GENRES.get(genre, "Unknown") for genre in query["genre_ids"]
            )

            query_results.append({"title":title, "director":director, "release_year":release_year, "rating":int(rating), "img_url":img_url, "genres":genres})

        return query_results




# for x in QueryMovie("spider-man").get_all():
#     print(x["title"])


# {
#   "page": 1,
#   "results": [
#     {
#       "adult": false,
#       "backdrop_path": "/snYOXem8pUGOffnLbbGq4aB1pg4.jpg",
#       "genre_ids": [
#         28,
#         80,
#         53
#       ],
#       "id": 1291608,
#       "title": "Dhurandhar",
#       "original_language": "hi",
#       "original_title": "धुरंधर",
#       "overview": "In the early 2000s, an undercover operative infiltrates Karachi's underworld, breaking into its inner circle to dismantle a violent nexus from within.",
#       "popularity": 8.4424,
#       "poster_path": "/8FHOtUpNIk5ZPEay2N2EY5lrxkv.jpg",
#       "release_date": "2025-12-05",
#       "softcore": false,
#       "video": false,
#       "vote_average": 7.33,
#       "vote_count": 355
#     },