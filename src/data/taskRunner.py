from computations import relevanceFeedback as rf
from data import DataHandler
import time
from computations import tasksBusiness as tb
import numpy as np

def task1_2CombinedPredictor(userid):
    movieid_name_map = DataHandler.movieid_name_map
    enter_userid = userid  # input("UserID : ")
    userId = int(enter_userid)
    times = time.time()
    DataHandler.vectors()
    DataHandler.createDictionaries1()
    rf.loadBase(userId)
    similarities = rf.runAllMethods(userid)
    movies = [rf.nonwatchedList[i] for i in similarities][0:5]
    moviesWatched_timestamp = list(DataHandler.user_rated_or_tagged_date_map.get(userId))
    
    moviesWatched_timestamp = sorted(moviesWatched_timestamp,key=itemgetter(1))
    moviesWatched_timestamp_sorted = list(list(zip(*moviesWatched_timestamp ))[0])
    watchedMovieNames = [movieid_name_map[movieid] for movieid in moviesWatched_timestamp_sorted]
    print('Movies Watched by the user in order: '+ str(watchedMovieNames))
    named_movies = [movieid_name_map[i] for i in movies]
    print('Top 5 movies : ' + str(named_movies))
    while True:
        feedback = input("Relevance (1/0) for each of the 5 movies: ")
        if feedback == 'exit':
            print("GoodBye........")
            break
        feedback = [int(i) for i in feedback.split(',')]
        new_query = rf.runAllMethodrelevancefeedback(movies, feedback)
        print([movieid_name_map[rf.nonwatchedList[i]] for i in new_query][0:5])


def task1_2Decompostions(func, userid):
    movieid_name_map = DataHandler.movieid_name_map
    enter_userid = userid  # input("UserID : ")
    userId = int(enter_userid)
    times = time.time()
    DataHandler.vectors()
    DataHandler.createDictionaries1()
    rf.loadBase(userId)
    rf.runDecomposition(func)

    new_query = rf.q_vector
    movies = rf.recommendMovies(new_query)
    named_movies = [movieid_name_map[i] for i in movies]
    print('Top 5 movies : ' + str(named_movies))
    while True:
        feedback = input("Relevance (1/0) for each of the 5 movies: ")
        if feedback == 'exit':
            print("GoodBye........")
            break
        feedback = [int(i) for i in feedback.split(',')]
        new_query = rf.newQueryFromFeedBack(movies, feedback)
        print([movieid_name_map[rf.nonwatchedList[i]] for i in new_query][0:5])
        # print(str(new_query) + "\n")

def task1_2PCA():
    userid = input("UserID : ")
    task1_2Decompostions(rf.loadPCASemantics, userid)


def task1_2SVD():
    userid = input("UserID : ")
    task1_2Decompostions(rf.loadSVDSemantics, userid)


def task1_2CP():
    userid = input("UserID : ")
    task1_2Decompostions(rf.loadCPSemantics, userid)


def task1_2Combined():
    userid = input("UserID : ")
    task1_2CombinedPredictor(int(userid))
    
def task1_2PageRank():
    userid = input("UserID : ")
    DataHandler.vectors()
    enter_userid = userid  # input("UserID : ")
    userId = int(enter_userid)
    DataHandler.createDictionaries1()
    rf.loadBase(userId);
    rf.task1d(userId)
    
def task3() :
    tb.task3();

def task1_2LDA(userid):
    movieid_name_map = DataHandler.movieid_name_map
    enter_userid = userid  # input("UserID : ")
    userId = int(enter_userid)
    DataHandler.vectors()
    DataHandler.createDictionaries1()
    rf.loadBase(userId)
    finalWeights = rf.finalWeights
    
    
    movie_movie_similarity_subset_new = rf.runLDADecomposition(userid)#update
    sim = list(movie_movie_similarity_subset_new.T.dot(finalWeights).astype(np.float32))
    movieList = list(movie_movie_similarity_subset_new.columns)
    simSorted = list(np.sort(sim)[::-1])[:5]
    simArgSorted = list(np.argsort(sim)[::-1])
    movies = [movieList[i] for i in simArgSorted][:5]
    named_movies = [movieid_name_map[movie] for movie in movies]
    watchedMovieNames = [movieid_name_map[movieid] for movieid in rf.moviesWatched]
    print(watchedMovieNames)
    print("---------------------------------------------")
    print('Top 5 movies and their similarity scores: \n' +str(list(zip(named_movies,simSorted)))+"\n")
    wantFeedback = True
    while wantFeedback:
        feedbackWant = input("Would you like to give feedback 'Y'/'N': ")
        if feedbackWant == 'Y':
            LDAFeedback(movies)
            wantFeedback = True
        elif feedbackWant == 'N':
            wantFeedback = False
            break
        else:
            print("Invalid Input provided. Please try again.")
            wantFeedback = True
    
def LDAFeedback(movies): 
    takeFeedback = True
    r = len(movies)
    while takeFeedback:
        feedback = input("Relevance (1/0) for each of the "+ str(r) +" movies: ")
        feedback_split = feedback.split(',')
        if len(feedback_split) != len(movies):
            print("Invalid Feedback string. Please give feedback for each of the movies.\n")
            takeFeedback = True
            continue
        elif any(isinstance(x, int) for x in feedback_split):
            print("Invalid Feedback string.\n")
            takeFeedback = True
            continue
        else:
            feedback = np.array([int(i) for i in feedback_split])
            if not ((feedback<= 1 ).sum() == feedback.size):
                print("Invalid Feedback string.\n")
                takeFeedback = True
                continue
            elif not ((feedback>= 0 ).sum() == feedback.size):
                print("Invalid Feedback string.\n")
                takeFeedback = True
                continue
            else:
                takeFeedback = False
    movieid_name_map = DataHandler.movieid_name_map
    lda_sem_matx=DataHandler.load_movie_LDASpace_df()
    new_query = rf.newQueryFromFeedBackLDA(movies, feedback,lda_sem_matx)#update
    print([movieid_name_map[rf.nonwatchedList[i]] for i in new_query[0]][0:5])
    
def load_dataForClassifiers():
    return rf.loadPCASemantics()
