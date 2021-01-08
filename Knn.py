import pandas as pd
import numpy as np
import math



class KNN:
    def __init__(self,movies,links,ratings,tags):
        self.movies = movies
        self.links = links
        self.ratings = ratings
        self.tags = tags
        self.processedData = pd.DataFrame()
    
    
    def extract_imp_movie_data(self):
    
        movies = {}
    
        for indRating,rating in self.ratings.iterrows():
            if rating['movieId'] in movies:
                movies[rating['movieId']] = {"value":movies[rating['movieId']]['value'] + rating['rating'],
                                              'count':movies[rating['movieId']]['count'] + 1 } 
            else:
                movies[rating['movieId']] = {'value':rating['rating'],"count":1}  
        
        self.filter_movies = movies            
    
    def set_average_ratings(self):
    
        average_ratings = []
    
        for key in self.filter_movies:
            average = self.filter_movies[key]['value'] / self.filter_movies[key]['count']
            average_ratings.append(average/5)
        
        self.processedData['ratings'] = average_ratings


    def gen_unique_genres(self):
        genres = set() 
        for index,movie in self.movies.iterrows():
            if movie['movieId'] in self.filter_movies:
                genre = movie['genres'].split('|')         
                for item in genre:
                    genres.add(item)
        return list(genres)
      
    
    def set_genres(self):
    
        unique_genres = self.gen_unique_genres()
        
        for genre in unique_genres:
            self.processedData['genre_' + genre] = [0] * len(self.filter_movies)
            
        for index,movie in self.movies.iterrows(): 
            if movie['movieId'] in self.processedData['movieId']:       
                movie_genres = movie['genres'].split('|')
                for genre in unique_genres:
                    if genre in movie_genres:
                        self.processedData['genre_' + genre][index] = 1 
    
    def set_movie_Ids(self):
        self.processedData['movieId'] = self.filter_movies.keys()
                
    
    def set_tags(self):
        
        unique_tags = set()
        for item in self.tags['tag']:
            unique_tags.add(item.lower())
        unique_tags = list(unique_tags)
        
        self.processedData['movieId'] = self.filter_movies.keys()
        
        for tag in unique_tags:
            self.processedData['tag_' +tag ] = [0] * len(self.filter_movies) 
        
        for index,movie in self.processedData.iterrows():
            movieId = movie['movieId']
            tags = self.tags[self.tags['movieId'] == movieId]
            if not tags.empty:
                for tag in tags['tag']:
                    self.processedData['tag_' + tag.lower()][index] = 1

    

    
    def calculate_euclidean_distance(self,point1,point2):
        independent_vars = point1.shape[0]
        sum_of_distances =  0
        for i in range(0,independent_vars):
            diff = point1[i] - point2[i]
            sum_of_distances += (diff ** 2)
        
        return math.sqrt(sum_of_distances)
    
    def recommend_movies(self,imdb_movieId,neighbours=7):
        
        movieId = self.links[self.links['imdbId'] == imdb_movieId]['movieId'].values[0]
        movie = self.processedData[self.processedData['movieId'] == movieId].iloc[:,1:].values[0]

        all_distances = [] 
        calculate_dataframe = self.processedData.iloc[:,1:]  
        for i in range(0,calculate_dataframe.shape[0]):
            distance = self.calculate_euclidean_distance(calculate_dataframe.iloc[i].values
                                                         ,movie)
            
            if distance != 0:
                all_distances.append((distance,i))
        
        
        print(sorted(all_distances)[0:neighbours])
        
        movie_ids = []
        
        for distance,index in sorted(all_distances)[:neighbours]:
            movie_ids.append(self.processedData.iloc[index,0])
        
        imdb_ids = self.links[self.links['movieId'].isin(movie_ids)]['imdbId'].values
        
        test = self.movies[self.movies['movieId'].isin(movie_ids)]
        print(test)
            
        return (imdb_ids)