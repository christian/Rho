import cPickle
import numpy as N
from operator import itemgetter

class Recommender:
    def __init__(self, user_features_file, movie_features_file):
        self.uf = user_features_file
        self.mf = movie_features_file

    def recommend(self, user):
        FILE = open(self.uf, 'r')
        userFeatures = cPickle.load(FILE)
        FILE.close()
    
        FILE = open(self.mf, 'r')
        moviesFeatures = cPickle.load(FILE)
        FILE.close()
        
        max_movies = moviesFeatures.shape[1]
        features = moviesFeatures.shape[0]
        ratings = dict()
        for movie_id in xrange(max_movies):
            ratings[movie_id] = 0.0
            for i in xrange(features):
                ratings[movie_id] += userFeatures[i][user] * moviesFeatures[i][movie_id]

        items = ratings.items()
        items.sort(key=itemgetter(1), reverse=True)
        for i, v in enumerate(items):
            if i > 10: break
            print "Movie: %s. Predicted rating: %s" % (v[0], v[1])
        
        
if __name__ == "__main__":
    user_feature_file = 'results/userFeatures_17-06-2010_16:35.txt'
    movie_feature_file = 'results/movieFeatures_17-06-2010_16:35.txt'
    
    rec = Recommender(user_feature_file, movie_feature_file)
    rec.recommend(1)