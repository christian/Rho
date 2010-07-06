import numpy as N
import cPickle
import sqlite3

SQLITE3_DB_PATH = 'results/results.sqlite3'

class Analyzer:
    def __init__(self, test_cases, sqlite_db):
        """
        Constructor. The test_cases param is used for specifying the training and test files. An example is given bellow:
        
        tests_cases = [
            {
             'test_dataset' : 'dataset/u1.test', 
             'user_features_file' : 'results/userFeatures_20-06-2010_17:11.txt', 
             'movie_features_file' : 'results/movieFeatures_20-06-2010_17:11.txt'
             }
        ]
        
        If test_cases is None, the training and test files are taken from the sqlite_db given as a parameter. 
        """
        self.results_db = sqlite_db
        # A test case contains more 3-uples of form (user_feature_file, movie_feature_file, test_database) in a hash format
        if not test_cases == None:
            self.test_cases = test_cases

    def read_features(self, users_features_file, movie_feature_file):
        """
        Read userFeatures and movieFeatures from the corresponding files given as parameters
        """
        FILE = open(users_features_file, 'r')
        userFeatures = cPickle.load(FILE)
        FILE.close()
    
        FILE = open(movie_feature_file, 'r')
        moviesFeatures = cPickle.load(FILE)
        FILE.close()
    
        return userFeatures, moviesFeatures

    def analyze(self, users_features_file, movie_feature_file, test_database):
        """
        Analyzes a pair of (userFeatures, movieFeatures) against a test_database in terms of prediction accuracy
        """
        FILE = open(test_database, 'r')
        
        userFeatures, moviesFeatures = self.read_features(users_features_file, movie_feature_file)
        
        total = 0
        correct = 0
        for movie_line in FILE.readlines():
            movie_line = movie_line.rstrip()
            (user_id, movie_id, rating, date) = movie_line.split("\t",  3)
            user_id = int(user_id)
            movie_id = int(movie_id)
            rating = int(rating)
        
            predicted_rating = 0.0
            for i in range(userFeatures.shape[0]):
                predicted_rating += userFeatures[i][user_id] * moviesFeatures[i][movie_id]
        
            total += 1
            err = abs(predicted_rating - rating)
            if err < 1:
                correct += 1
        return (total, correct)
    
    def test_files(self):
        """
        test each pair given as parameter in the constructor, via self.test_cases
        """
        for test_case in self.test_cases:
            self.test(test_case['user_features_file'], test_case['movie_features_file'], test_case['test_database'])
            
    def test_from_sql(self):
        """
        test each file pair in the sqlite3 database
        """
        conn = sqlite3.connect(SQLITE3_DB_PATH)
        c = conn.cursor()
        c.execute('select * from results')
        for row in c:
            # date | algorithm | epochs | features | running_time | RMSE | training_dataset | test_dataset | match
            users_features_file = "results/userFeatures_" + row[0] + ".txt"
            movie_features_file = "results/movieFeatures_" + row[0] + ".txt"
            test_database       = row[7]

            percent_match = self.test(users_features_file, movie_features_file, test_database)
            
            u = conn.cursor()
            u.execute('update results set match=? where date=?', (percent_match, row[0], ))
            conn.commit()
        u.close()
        c.close()
        conn.close()
        

    def test(self, users_features_file, movie_features_file, test_database):
        print ''
        print "TEST: "
        print "---------------------------------------------------"
        print "Users  features: " + users_features_file
        print "Movies features: " + movie_features_file
        print "Test db: " +         test_database
        
        print "Analyzing results ... "
        total, correct = self.analyze(users_features_file, movie_features_file, test_database)
        
        percent_match = ((100.0 * float(correct)) / float(total))
        print "Match: ", ((100.0 * float(correct)) / float(total)) , "%"
        
        return percent_match
        
tests_cases = [
    {
     'test_dataset' : 'dataset/u1.test', 
     'user_features_file' : 'results/userFeatures_20-06-2010_17:11.txt', 
     'movie_features_file' : 'results/movieFeatures_20-06-2010_17:11.txt'
     }
]

if __name__ == "__main__":
    """
    The purpose of this utility is to analyze how efficient is a predicted model for a test dataset. 
    It uses the Analyzer class.
    """
    analyzer = Analyzer(tests_cases, "results/results.sqlite3")
    # analyzer = Analyzer(None)
    analyzer.test_from_sql()
    
    print "Done."

