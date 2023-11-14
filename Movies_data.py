import requests
import json
import time

############################## id to genre ################################
def id_to_genre(movie,dict_id) :
    names = []
    for g in movie["genre_ids"] :
        genre = [d for d in dict_id if d['id'] == g]
        names.append(genre[0]['name'])
    movie["genre_names"] = names

##############################  get genre  #################################
def get_genre():
    url_genre = "https://api.themoviedb.org/3/genre/movie/list?language=en"

    headers_genre = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmZmYzMjliNzY3NzIyZTY1OGI1NGQ4Njg2ZTRjNjAzZSIsInN1YiI6IjY1NGNlZmU4NWE1ZWQwMDBlM2Y1OWM1YyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.XcYk2ynESoWu5jo6lJSYQBlZ3gXkjC1na9f8_DMwyGE"
    }

    response_genre = requests.get(url_genre, headers=headers_genre).json()

    response_genre = response_genre["genres"]

    return response_genre

################################### get Moviesinformation ########################
def get_movies(page):
    API_KEY = 'fff329b767722e658b54d8686e4c603e'
    MOVIE_ENDPOINT = "https://api.themoviedb.org/3/movie/popular?api_key={}&page={}"

    response = requests.get(MOVIE_ENDPOINT.format(API_KEY,page))
    return  response.json()


dict_ids = get_genre()
movies  = get_movies(1)


for result in movies["results"] :
    id_to_genre(result,dict_ids)
    print(result)
    # save to file json :
    with open('json_files/movies.json', 'a') as outfile:
        json.dump(result, outfile)
        outfile.write('\n')
