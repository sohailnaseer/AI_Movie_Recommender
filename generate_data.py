import pandas as pd
import Knn


movies_dataframe = pd.read_csv('movies.csv')
links_dataframe = pd.read_csv('links.csv')
ratings_dataframe = pd.read_csv('ratings.csv')
tags_dataframe = pd.read_csv('tags.csv')


recommender = Knn.KNN(movies_dataframe,links_dataframe,ratings_dataframe,tags_dataframe)
recommender.extract_imp_movie_data()
recommender.set_movie_Ids()
recommender.set_average_ratings()
recommender.set_genres()
recommender.set_tags()



recommender.processedData.to_csv(r'E:\WhoAmI\University Work\Semsester 5\Aritifical Intelligence\Movie Recommender System\server\processed_data.csv',index=None,header=True)