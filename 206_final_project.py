# Jacob Kreinik SI 206 Final Project 
# Option 2

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


#-------------------------------------------- Twitter Tweets -----------------------------------------#

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

#pprint (tweet_data_tup_lst)

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

	


#--------------------------------------------Twitter Users-----------------------------------------------------

twitter_user_CACHE_FNAME = "Twitter_user_cache.json"

try: 
	twitter_user_cahche_file = open(twitter_CACHE_FNAME, 'r')
	twitter_user_cache_contents = twitter_cahche_file.read()
	twitter_user_cahche_file.close()
	twitter_user_CACHE_DICTION = json.loads(twitter_cache_contents)
except: 
	twitter_user_CACHE_DICTION = {} 


actor_search_tweets = [actor_1_tweets, actor_2_tweets, actor_3_tweets]
#pprint (actor_search_tweets[0][0]['user'])

twitter_user_data = []
for x in actor_search_tweets: 
	for user in x: 
		user_id_str = user['user']['id_str']
		user_screename = user['user']['screen_name']
		user_num_favs = user['user']['favourites_count']
		user_num_followers = user['user']['followers_count']
		user_location = user['user']['location']


		twitter_user_tup = (user_id_str, user_screename, user_num_favs, user_num_followers, user_location)
		twitter_user_data.append(twitter_user_tup)

		if user_screename not in twitter_user_CACHE_DICTION: 
			twitter_user_CACHE_DICTION[user_screename] = user['user']
			twitter_user_cahche_file = open(twitter_user_CACHE_FNAME, 'w')
			twitter_user_cahche_file.write(json.dumps(twitter_user_CACHE_DICTION))
			twitter_user_cahche_file.close()

for x in actor_search_tweets: 
	for user in x: 
		users = user['entities']['user_mentions']	
		for a in users: 
			user_mentions = api.get_user(a['screen_name']) 
			user_id_str = user_mentions['id_str']
			user_screename = user_mentions['screen_name']
			user_num_favs = user_mentions['favourites_count']
			user_num_followers = user_mentions['followers_count']
			user_location = user_mentions['location']

			twitter_user_tup = (user_id_str, user_screename, user_num_favs, user_num_followers, user_location)	
			twitter_user_data.append(twitter_user_tup)

			if a['screen_name'] not in twitter_user_CACHE_DICTION: 
				twitter_user_CACHE_DICTION[user_screename] = user_mentions
				twitter_user_cahche_file = open(twitter_user_CACHE_FNAME, 'w')
				twitter_user_cahche_file.write(json.dumps(twitter_user_CACHE_DICTION))
				twitter_user_cahche_file.close()

#pprint (twitter_user_data)		

#---------------------------------------- Twitter User SQL -------------------------------------#		
conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Users') 

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Users (user_id_str TEXT PRIMARY KEY, '
table_spec += 'screen_name TEXT, user_num_favs INTEGER, user_num_followers INTEGER, user_location TEXT)'
cur.execute(table_spec)


statement = 'INSERT or IGNORE INTO Users VALUES (?, ?, ?, ?, ?)'

for a in twitter_user_data: 
	cur.execute(statement, a)
conn.commit()

	

#------------------------------------------- Queries ----------------------------------------
cur.execute('SELECT screen_name, user_num_followers FROM Users WHERE user_num_followers > 10000')
high_follower_count = cur.fetchall()

cur.execute('SELECT Movies.lead_actor, Tweets.num_retweets FROM Movies INNER JOIN Tweets ON Movies.lead_actor = Tweets.actor_search') 
movie_data = cur.fetchall()

cur.execute('SELECT user_num_followers, user_num_favs, screen_name FROM Users WHERE user_num_followers > user_num_favs')
high_follower_to_fav_ratio = cur.fetchall()

cur.execute('SELECT tweet_text FROM Tweets') 
all_tweets = cur.fetchall()

cur.execute('SELECT num_retweets FROM Tweets')
all_retweets = cur.fetchall() 



#------------------------------------------- Data Processing ----------------------------------
# Number 1: Sorting 

top_tweeters = sorted(high_follower_count, key = lambda x: x[1], reverse = True)
data_process_1 = 'Here is a list of users that have over 10,000 followers. To see which one of these users has the most influence, they have been sorted from most followers to least followers. The format is (screen_name, num_followers). The list is as follows: \n' + str(top_tweeters)

print ('------------------------- Data Processing 1 Sorting --------------------------')
print (data_process_1)
print('\n\n')

#Number 2: Data mapping 

def get_follower_to_fav_ratio(x):
	if x[1] != 0:
		ratio = (x[0])/(x[1])
		return (ratio, x[2]) 

fav_ratio = map(get_follower_to_fav_ratio, high_follower_to_fav_ratio)
fav_ratio_lst = []
for x in fav_ratio: 
	ratio_screename = x
	fav_ratio_lst.append(ratio_screename)

	
data_process_2 = 'Here is a list of users that have more followers than total favorites. This means that their influence on twitter is greater than their usage of twitter: \n' + str(fav_ratio_lst)
print ('------------------------- Data Processing 2 Mapping --------------------------')
print(data_process_2)
print ('\n\n')

#Number 3 Dictionary accumulation 
total_actor_retweets = {}

for x in movie_data: 
	if x[0] not in total_actor_retweets: 
		total_actor_retweets[x[0]] = x[1]
	else: 
		total_actor_retweets[x[0]] += x[1]

data_process_3 = 'Here is a dictionary with actors as keys and total number of retweets based on those actors as values. We can see what actor has accumulated the most retweets on all tweets generated about them. The dictionary is as follows: \n' + str(total_actor_retweets)		
			

print ('------------------------- Data Processing 3 Dictionary accumulation --------------------------')
print(data_process_3)
print ('\n\n')

#Number 4 list comprehension/ zip function 

length_of_tweet = [len(x[0]) for x in all_tweets] 
retweets_of_tweet = [x[0] for x in all_retweets]
zip_length_and_num_retweets = zip(length_of_tweet, retweets_of_tweet) 
length_and_num_retweets = [x for x in zip_length_and_num_retweets]

data_process_4 = 'Here is a list of two element tuples. The first element in the tuple represents the length of a tweet and the second element represents the number of retweets. I wanted to see if there was a correlation between these two elements. The tuple is as follows: \n' + str(length_and_num_retweets)

print ('------------------------- Data Processing 4 list comprehension/ zip function -------------------')
print(data_process_4)

conn.close()

#---------------------------------- Text File ------------------------------------------
text_file = 'final_project_output.txt'
t_file = open(text_file, 'w')
t_file.write('Jacob Kreinik Final Output SI 206 W17 Final Project' + '\n\n')
t_file.write(data_process_1 + '\n\n')
t_file.write(data_process_2 + '\n\n')
t_file.write(data_process_3 + '\n\n')
t_file.write(data_process_4 + '\n\n')
t_file.close()

#-------------------------------- Test Cases -------------------------------------------
class Tests(unittest.TestCase): 
	def test_type_omdb_api_call_and_cache(self):
		x = omdb_api_call_and_cache('step brothers')
		self.assertEqual(type(x),type({}))
	def test_movie_constructor(self): 
		x = Movie(movie_1) #step brothers
		self.assertEqual(type(x.imdb_rating), float) 
	def test_movie_constructor_2(self): 
		x = Movie(movie_1) #step brothers
		self.assertEqual((x.director), 'Adam McKay') 
	def test_movie_get_all_actors(self): 
		x = Movie(movie_1) #step brothers
		self.assertEqual(type(x.get_all_actors()), type([])) 	
	def test_movie_get_lead_actor(self): 
		x = Movie(movie_1) #step brothers
		self.assertEqual(x.get_lead_actor(),'Will Ferrell') 
	def test_movie_get_title(self): 
		x = Movie(movie_1) #step brothers
		self.assertEqual((x.get_title()), 'Step Brothers')
	def test_movie_get_num_lang(self): 
		x = Movie(movie_1) #step brothers
		self.assertEqual(type(x.get_num_lang()), int)
	def test_movie_get_imdb_id(self): 
		x = Movie(movie_1) #step brothers
		self.assertEqual(type(x.get_imdb_id()), str) 	 	 			
	def test_get_movie_data(self):
		x = get_movie_data(movie_obj_lst) #invoking the function with a list of the three movie objects 
		self.assertEqual(type(x), type([]))
		self.assertEqual(type(x[0]), tuple)
	def test_get_twitter_data(self): 
		x = get_twitter_data('Will Ferrell')
		self.assertEqual(type(x[0]), type({}))
	def test_movie_sql(self): 
		conn = sqlite3.connect('final_project.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies')
		result = cur.fetchall()
		self.assertTrue(len(result[0]), 6)
		conn.close() 
		



if __name__ == "__main__":
	unittest.main(verbosity=2)		

 
			
























