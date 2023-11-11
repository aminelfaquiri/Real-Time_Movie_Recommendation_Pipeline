import time 
import json 
from datetime import datetime
from Movies_data import get_movies,id_to_genre,get_genre
from kafka import KafkaProducer

# Messages will be serialized as JSON 
def serializer(message):
    return json.dumps(message).encode('utf-8')

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

dict_ids = get_genre()
page = 1

if __name__ == '__main__':

    while True:

        movies = get_movies(page)

        print("#"*30)
        print(page)
        print("#"*30)

        if movies is not None:
            for result in movies["results"] :
                id_to_genre(result,dict_ids)
                time.sleep(2)

                # Send the data to the 'movies' topic:
                print(f'Producing message @ {datetime.now()} | Message = {str(result["original_title"])}')
                producer.send('movies', result)
        else :
            print("API request failed.")
        page += 1