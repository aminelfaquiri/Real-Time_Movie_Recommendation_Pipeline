# Real Time Movie Recommendation Pipeline

## Introduction
As a Data Developer, my task is to construct a real-time system that spans from collecting data from the movielens.org API to presenting recommendations to users. The project encompasses critical stages, with each step playing a pivotal role in the seamless functioning of the recommendation pipeline.

## Planification
![Planing](https://github.com/aminelfaquiri/Real-Time_Movie_Recommendation_Pipeline/assets/81482544/14e81881-50fc-41bb-98f4-5d410b43c406)

## Requirements Expression
1. **Kafka Configuration**:
Establishing a Kafka cluster and configuring producers to seamlessly transmit user interaction data to specific topics.

2. **SparkStreaming Processing**:
Creating pipelines to consume Kafka data, apply transformations, and forward them to Elasticsearch. These transformations include data enrichment, normalization, and custom transformations, enhancing data quality and relevance.

3. **Modelling and Storage in Elasticsearch**:
Designing data indices and models in Elasticsearch to efficiently store information about movies and users.

4. **Development of Recommendation API**:
Programming a RESTful API, utilizing a framework like Flask, to interact with Elasticsearch, retrieve, and serve personalized recommendations.

5. **Visualization with Kibana**:
Crafting dashboards in Kibana for visualizations that aid decision-making. Examples include visualizing movie release date distribution, top 10 popular movies, average ratings by genre, linguistic distribution of films, top 10 movies by votes, and the distribution of movie rankings.

## RGPD Compliance
look in the pdf file in repo files.

## Creating a Kafka Topic :
Initiate ZooKeeper by running: `_run ZooKeeper_`

Launch the Kafka Server with the command: `_run Kafka Server_`

Once the above steps are completed, I create a topic named "movies"

`kafka-topics --bootstrap-server 127.0.0.1:9092 --topic movies --create --partitions 3 --replication-factor 1`

## Create a Kafka Producer :
I have created a Python script that serves as the Kafka producer component in the Real-Time Movie Recommendation Pipeline. Its primary function is to collect movie data from the movielens.org API and send it to a Kafka topic named 'movies.

## Create SparkStreaming Traitement Consumer :
in create a script spark streeming by using python to get data from a producer kafka :
1. **Spark Session Creation:**
A Spark session is created to interact with Spark Streaming and Spark SQL. Necessary configurations and package dependencies, including those for Kafka and Elasticsearch, are specified.

2. **Define Schema for Movies Data:**
The schema for the movies data is defined to ensure proper parsing of the incoming data from Kafka.

3. **Read Data from Kafka:**
Spark Streaming is configured to read data from the "movies" Kafka topic.

4. **Deserialize and Parse Data:**
The received data is deserialized and parsed into a structured format using the defined schema.

4. **Perform the data transformation:**

* Create a new field called "description" by combining the "title" and "overview" fields.
* Normalize the "vote_average" and "popularity" fields from float, accepting only one decimal place.
* Convert the "release_date" field to the appropriate data type.

7. **Write Stream to Elasticsearch:**
The processed data is then written to Elasticsearch. The writeStream operation is used to append the data to the Elasticsearch index named "movies."
<img width="420" alt="image" src="https://github.com/aminelfaquiri/Real-Time_Movie_Recommendation_Pipeline/assets/81482544/3f947aab-ab2b-4d94-97eb-7b9205208921">


## Visualization with Kibana :
![dashboard](https://github.com/aminelfaquiri/Real-Time_Movie_Recommendation_Pipeline/assets/81482544/a44b1a3a-f8a6-4a85-a8e7-5702e21297fc)

## Creating the API Recommendation (Flask) :
![screencapture-127-0-0-1-5000-2023-11-16-15_20_28](https://github.com/aminelfaquiri/Real-Time_Movie_Recommendation_Pipeline/assets/81482544/1018e595-660c-42ca-9649-799587c4d122)

* **logic of my recomandation**
The logic of my recommendation system is based on a simple approach. I use a query DSL to retrieve movies that have at least one category (genre) and share the same or higher vote average, along with the same or greater popularity

## Challenges Faced :

**Configuration Issue:**
Facing a problem with the compatibility between Spark and Elasticsearch versions.

**Solusion :**
finely i foud the version correct for me is :
* Spark : 3.2.4
* Elasticseach : 8.11
* Scala : 2.12.15

## Conclusion :
In conclusion, the Real-Time Movie Recommendation Pipeline successfully implements a robust system for collecting, processing, and delivering personalized movie recommendations in real-time. The project, encompassing Kafka, SparkStreaming, Elasticsearch, Flask API, and Kibana visualization
