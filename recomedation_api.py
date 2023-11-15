from flask import Flask, jsonify
from urllib.parse import quote_plus

from elasticsearch import Elasticsearch

app = Flask(__name__)

# Connect to Elasticsearch
# es = Elasticsearch(['localhost:9200'])
es = Elasticsearch(['http://localhost:9200'])


def get_movie_recommendations(title):
    # Elasticsearch query to find a movie by title :
    query = {
        "query": {
            "match": {
                "title": title
            }
        }
    }

    response = es.search(index='movies', body=query)

    # Extract movie information from the response 
    if response['hits']['total']['value'] > 0 :
        movie_info = response['hits']['hits'][0]['_source']

        # Retrieve recommendations based on similar genres and high vote_average
        genre_ids = movie_info.get('genre_ids', [])
        vote_average = movie_info.get('vote_average', 0)

        # Elasticsearch query to find similar movies
        recommendation_query = {
            "query": {
                "bool": {
                    "must_not": [
                        {"match": {"title": title}}
                    ],

                    "filter": [
                        {"terms": {"genre_ids": genre_ids}},
                        {"range": {"vote_average": {"gte": vote_average}}}
                    ]
                }
            },
            "size": 5  # Adjust the number of recommendations as needed
        }

        recommendation_response = es.search(index='movies', body=recommendation_query)

        # Extract movie recommendations from the response
        recommendations = [hit['_source']['title'] for hit in recommendation_response['hits']['hits']]

        return {'recommendations': recommendations,'title': title}
        return {'title': title,'movie_info': movie_info,'recommendations': recommendations}
    else:
        return None

@app.route('/movie/<string:title>')
def get_movie_info(title):
    result = get_movie_recommendations(title)
    if result:
        return jsonify(result)
    else:
        return jsonify({'title': title, 'message': 'Movie not found'})

if __name__ == '__main__':
    app.run(debug=True)
