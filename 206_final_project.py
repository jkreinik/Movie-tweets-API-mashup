import unittest 
import tweepy 
import requests 
import json 
import twitter_info
import sqlite3
from pprint import pprint 


OMDB_FNAME = "OMDB_cache.json"

try: 
	omdb_cache_file = open(OMDB_FNAME, 'r')
	omdb_cache_contents = cache_file.read()
	omdb_cache_file.close()
	omdb_CACHE_DICTION = json.loads(omdb_cache_contents)
except: 
	omdb_CACHE_DICTION = {}


movie1 = input("Insert the 1st movie that you want to search for and hit enter ")
movie2 = input("Insert the 2nd movie that you want to search for and hit enter ")
movie3 = input("Insert the 3rd movie that you want to search for and hit enter ")
movie_search_terms = [movie1, movie2, movie3] #list of the movies that the user imputed 

def omdb_api_call_and_cache(movie):
	omdb_baseurl = 'http://www.omdbapi.com/?'
	omdb_fullurl = requests.get(omdb_baseurl, params = {'t': movie})
	#result = json.loads(omdb_fullurl.text) #object version of omdb dictionary
	#test = omdb_fullurl.text #string version of omdb dictionary

	if movie in omdb_CACHE_DICTION: 
		omdb_text = omdb_CACHE_DICTION[movie]
	else: 
		omdb_CACHE_DICTION[movie] = omdb_fullurl.text 
		omdb_text = omdb_fullurl.text 

		omdb_cache_file = open(OMDB_FNAME, 'w')
		omdb_cache_file.write(json.dumps(omdb_CACHE_DICTION))
		omdb_cache_file.close()

	return(json.loads(omdb_text))

movie_1 = omdb_api_call_and_cache(movie_search_terms[0])
movie_2 = omdb_api_call_and_cache(movie_search_terms[1])
movie_3 = omdb_api_call_and_cache(movie_search_terms[2])

movie_dics = [movie_1, movie_2, movie_3] #list of movie dictionaries 
#pprint (movie_dics[0])

# print (movies) #list of movie titles 

class Movie(): 
	def __init__(self, omdb_dic): 
		self.omdb_dic = omdb_dic
		self.imdb_rating = float(self.omdb_dic['imdbRating'])
		self.director = self.omdb_dic['Director'] 
		self.rated = self.omdb_dic['Rated']


	def get_all_actors(self): 
		actors = self.omdb_dic['Actors']
		actor_lst = actors.split(',')
		return actor_lst

	def get_lead_actor(self): 
		actor_lst = self.get_all_actors()
		lead_actor = actor_lst[0]
		return lead_actor	

	def get_title(self):
		return self.omdb_dic['Title']

	def get_release_date(self):
		return self.omdb_dic['Released']	 

	def get_num_lang(self): 
		lang_str = self.omdb_dic['Language']
		lang_lst = lang_str.split(',')	
		return len(lang_lst)

	def get_imdb_id(self):
		return self.omdb_dic['imdbID']	

	def __str__(self):
		title = self.get_title()
		director = self.director
		actor = self.get_lead_actor()
		rating = self.imdb_rating
		result = 'The name of the movie is: {} \n The director of the movie is: {} \n The leading actor is: {} \n The IMDB rating is: {}'.format(title, director, actor, rating)
		return result
			


movie_obj_lst = [] #list of movie objects using the dictionaries in movie_dics as input
for movie in movie_dics: 
	movie_object = Movie(movie)
	movie_obj_lst.append(movie_object) 
	

def get_movie_data(movie_lst):
	movie_data_tup_lst = []
	for movie in movie_obj_lst:  
		movie_id = movie.get_imdb_id()
		movie_director = movie.director
		movie_title = movie.get_title()
		movie_imdb_rating = movie.imdb_rating 
		movie_lead_actor = movie.get_lead_actor()
		movie_num_lang = movie.get_num_lang()

		movie_tup = (movie_id, movie_director, movie_title, movie_imdb_rating, movie_lead_actor, movie_num_lang)
		movie_data_tup_lst.append(movie_tup)

	return movie_data_tup_lst 


all_movie_data_tup = get_movie_data(movie_obj_lst)

#print (all_movie_data_tup)		

#---------------------------------------------Movie SQL---------------------------------------------------


conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Movies') 

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Movies (movie_id TEXT PRIMARY KEY, '
table_spec += 'director TEXT, title TEXT, imdb_rating INTEGER, lead_actor TEXT, num_languages INTEGER)'
cur.execute(table_spec)


statement = 'INSERT INTO Movies VALUES (?, ?, ?, ?, ?, ?)'

for a in all_movie_data_tup: 
	cur.execute(statement, a)
conn.commit()	


#-----------------------------------Twitter Tweets-----------------------------------------#

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, parser = tweepy.parsers.JSONParser())

twitter_CACHE_FNAME = "Twitter_cache.json"

try: 
	twitter_cahche_file = open(twitter_CACHE_FNAME, 'r')
	twitter_cache_contents = twitter_cahche_file.read()
	twitter_cahche_file.close()
	twitter_CACHE_DICTION = json.loads(twitter_cache_contents)
except: 
	twitter_CACHE_DICTION = {}

def get_twitter_data(search): 
	if search in twitter_CACHE_DICTION: 
		api_call = twitter_CACHE_DICTION[search]

	else: 
		api_call = api.search(q = search)
		twitter_CACHE_DICTION[search] = api_call 
		twitter_cahche_file = open(twitter_CACHE_FNAME, 'w')
		twitter_cahche_file.write(json.dumps(twitter_CACHE_DICTION))
		twitter_cahche_file.close()
	
	return api_call['statuses']



actor_search_1 = movie_obj_lst[0].get_lead_actor()
actor_search_2 = movie_obj_lst[1].get_lead_actor()
actor_search_3 = movie_obj_lst[2].get_lead_actor()

actor_1_tweets = get_twitter_data(actor_search_1) 
actor_2_tweets = get_twitter_data(actor_search_2) 
actor_3_tweets = get_twitter_data(actor_search_3) 
#pprint (actor_1_tweets)

tweet_dic_lst = [actor_1_tweets, actor_2_tweets, actor_3_tweets] #twitter dictionaries based off of 3 actor search terms
search_term_lst = [actor_search_1, actor_search_2, actor_search_3] #list of actor search terms
tweet_dic_lst = zip(tweet_dic_lst, search_term_lst) 


tweet_data_tup_lst = []
for x in tweet_dic_lst: 
	for tweet in x[0]:
		id_str = tweet['id_str']
		user_id = tweet['user']['id_str']
		text = tweet['text']
		num_retweets = tweet['retweet_count']
		num_favs = tweet['favorite_count']
		movie_search = x[1]

		tweet_tup = (id_str, user_id, text, num_retweets, num_favs, movie_search)
		tweet_data_tup_lst.append(tweet_tup) 

pprint (tweet_data_tup_lst)

#---------------------------------------------Tweets SQL---------------------------------------------------


conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets') 

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Tweets (id_str TEXT PRIMARY KEY, '
table_spec += 'user_id TEXT, tweet_text TEXT, num_retweets INTEGER, num_favs INTEGER, actor_search TEXT)'
cur.execute(table_spec)


statement = 'INSERT or IGNORE INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'

for a in tweet_data_tup_lst: 
	cur.execute(statement, a)
conn.commit()

conn.close()	


#--------------------------------------------Twitter Users-----------------------------------------------------












