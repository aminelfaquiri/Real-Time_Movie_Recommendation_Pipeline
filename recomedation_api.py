from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from elasticsearch import Elasticsearch
import secrets

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = secrets.token_hex(16)


# Connect to Elasticsearch
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

    # Extract movie information from the response  :
    if response['hits']['total']['value'] > 0 :
        movie_info = response['hits']['hits'][0]['_source']

        # remove the field not importente :        
        del movie_info["adult"]
        del movie_info["overview"]
        del movie_info["backdrop_path"]
        del movie_info["original_title"]
        del movie_info["video"]
        del movie_info["description"]
        # del movie_info["poster_path"]

        ######################## Recomendation Movies ######################################

        # Elasticsearch query to find similar movies
        recommendation_query = {
            "query": {
                "bool": {
                    "must_not": [
                        {"match": {"title": title}}
                    ],

                    "filter": [
                        {"terms": {"genre_ids": movie_info.get('genre_ids', [])}},
                        {"range": {"vote_average": {"gte": movie_info.get('vote_average', 0)}}},
                        {"range": {"popularity": {"gte": movie_info.get('popularity', 0)}}}
                    ]
                }
            },
        }

        recommendation_response = es.search(index='movies', body=recommendation_query,size=5)

        Movies = []
        # Extract movie recommendations from the response :
        recommendations = [hit['_source'] for hit in recommendation_response['hits']['hits']]

        for movie in recommendations :
            del movie["adult"]
            del movie["genre_ids"]
            del movie["overview"]
            del movie["backdrop_path"]
            del movie["original_title"]
            del movie["video"]
            del movie["description"]
            # del movie["poster_path"]
            Movies.append(movie)

        # #####################################################################################
        return {'Your Movies': movie_info,'recommendations': Movies}
    else:
        return None

# ############################ Inpute ###############################
class MovieForm(FlaskForm):
    movie_name = StringField('Movie Name', validators=[DataRequired()])
    submit = SubmitField('Get Recommendations')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MovieForm()
    result = None

    if form.validate_on_submit():
        movie_name = form.movie_name.data
        result = get_movie_recommendations(movie_name)

    return render_template('index.html', form=form, result=result)

@app.route('/movie/<string:title>')
def get_movie_info(title):
    result = get_movie_recommendations(title)
    if result:
        return jsonify(result)
    else:
        return jsonify({'title': title, 'message': 'Movie not found'})

if __name__ == '__main__':
    app.run(debug=True)
