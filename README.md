# Real-Time_Movie_Recommendation_Pipeline

## Introduction
As a Data Developer, my task is to construct a real-time system that spans from collecting data from the movielens.org API to presenting recommendations to users. The project encompasses critical stages, with each step playing a pivotal role in the seamless functioning of the recommendation pipeline.

## Planification
Outline the plan or roadmap for the project, including milestones and key tasks.

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
i create Python script serves as the Kafka producer component in the Real-Time Movie Recommendation Pipeline. Its primary function is to collect movie data from the movielens.org API and send it to a Kafka topic named "movies."

## Create SparkStreaming Traitement Consumer :
in create a script spark streeming by using python to get data from a producer kafka :
1. **Spark Session Creation:**
A Spark session is created to interact with Spark Streaming and Spark SQL. Necessary configurations and package dependencies, including those for Kafka and Elasticsearch, are specified.

3. **Define Schema for Movies Data:**
The schema for the movies data is defined to ensure proper parsing of the incoming data from Kafka.

5. **Read Data from Kafka:**
Spark Streaming is configured to read data from the "movies" Kafka topic.

7. **Deserialize and Parse Data:**
The received data is deserialized and parsed into a structured format using the defined schema.

9. **Write Stream to Elasticsearch:**
The processed data is then written to Elasticsearch. The writeStream operation is used to append the data to the Elasticsearch index named "movies."
<img width="960" alt="image" src="https://github.com/aminelfaquiri/Real-Time_Movie_Recommendation_Pipeline/assets/81482544/5abc0b19-98c4-4149-8307-39bd12080297">

## Visualization with Kibana :

## Creating the API Recommendation (Flask) :
the get_movie_recommendations function acts as the core logic for handling movie recommendation requests. It interacts with Elasticsearch to retrieve information about the specified movie and formulates additional queries to find and extract relevant movie recommendations.

* **logic of my recomandation**
i use the simple logic is the 

<img width="390" alt="Capture d'écran 2023-11-14 225229" src="https://github.com/aminelfaquiri/Real-Time_Movie_Recommendation_Pipeline/assets/81482544/327c0b70-0c64-42b2-a689-a44dc529de66">

## les difficultés rencontrées :
* probleme the version between elasticsearch and spark and scala.
## Conclusion :

