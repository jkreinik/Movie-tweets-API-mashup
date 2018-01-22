What option did you pick? 
Option 2 

What does it do? 
This program takes in 3 movies that the user selects and generates data based on those three movies. Then, using the main actor of the movie, it searches twitter and generates data based on those search terms on twitter. Then the program puts the movie data and twitter data into three different data bases and processes this data.

How do you run it?
on terminal use the command: python 206_final_project.py

What are the dependencies? 
•	Twitter_info file with consumer key, consumer secret, access token, and access token secret. 
•	Install pip 
•	Install tweepy 
•	Install sqlite3 

Files included 
•	206_final_project.py 
		-final project with finished code 

•	final_project.db 
		-a data base file that has three different tables (Movies, Tweets, Users)

•	OMDB_cache.json 
		-A dictionary file in json format of the information from the omdb api 

•	Twitter_cache.json 
		-A dictionary file in json format of the information on tweets from the twitter api 

•	Twitter_user_cache.json 
		-A dictionary file in json format of the information about the users from the twitter api 

•	Final_project_output.txt 
		-A txt file containing the output from my four data processing techniques 

•	Screenshots of git commits 
		-Proof of output and git commits

•	screenshots of terminal output
		-proof of terminal output

•	final_read_me.txt
		-this document

Function descriptions 

• omdb_api_call_and_cache 
	-input: a required movie title that is a str.  
	-rerurn value: this function returns an ombd dictionary that contains all information about a the movie that was inputted 
	-behavior: This function takes in a movie search term and then returns an omdb dictionary. This dictionary is then used as an input for the movie class. Additionally, the function caches the movie dictionary into a file called OMDB_cache.json. 

• get_movie_data 
	-input: a required list of Movie Objects  
	-return value: a list of tuples. each tuple in the list is information about a specific movie in the inputed list 
	-behavior: This takes a list of movie objects and using the methods of the movie class, gathers different attributes about the movie and puts it into a tuple. this tuple is then appended to a list that is returned. 

• get_twitter_data
	input: a term that will search twitter. In the case of the program this is the name of an actor as a str 
	return value: a list of twitter information dictionaries based on the search term. This is information on tweets as well as users 
	behavior: this function takes an actor search term and generates a list of twitter information dictionaries. The function then caches the information on tweets in a file called Twitter_cache.json. 

• get_follower_to_fav_ratio 
	input: This function takes a tuple with three different elements in it. The first element an int that represents number of followers of a user, the second is an int that represents number of favorites of a user, and the third is a str that represents the screen name of a twitter user. 
	return value: This function returns a tuple with two elements. The first element is number of followers divided by number of favorites. and the second element is the screen name of the twitter user. 
	behavior: This function calculates the ratio of twitter followers to twitter users and then returns the ratio and the assosiated user in a tuple

Class descritiopns: 

• Movie 
-Instance: Represents a movie and all the information about it. 

-Input: This class requires a correctly formatted json dictionary that is about a specific movie. In my program, the function mdb_api_call_and_cache returns this type of dictionary when given a specific movie name. The constructor has four instance variables. self.omdb represents the movie dictionary that is required. self.imbd rating is the imdb rating of the movie that is extracted from the ombd_dictionary. self.director represents the director of the movie and is extracted from the ombd_dic. self.rated represtents what the movie is rated ie pg-13, R. This is also extracted from the ombd_dic 

-Methods: 

• get_all_actors 
input: self
return value: a list of actor str's 
behavior: extracts a list of actors from the inputed ombd_dic. 

• get_lead_actor 
input: self
return value: an actor name as an str
behavior: gets the lead actor from the list of actors in get_all actors. The leade actor is just the first actor in that list 

• get_title: 
input: self
return value: The title of a movie as an str
behavior: gets the title of the movie from the inputted ombd_dic

• get_num_lang 
input: self
return value: an int of the number of languages in the movie 
behavior: gets the number of languages in the movie from the inputted ombd_dic 

• get_imdb_id
input: self
return value: a str of the imbd id 
behavior: gets the id of the movie from the inputted imbd_dic 

• __str__ 
input: self
return value: returns an str that highlights the different attributes about the movie
behavior: uses different methods to get information about the movie and returns a well written message telling what those different attributes are 

Database Creating 


Row representation:

•Movie Table
Row representation: A specific movie that is generated by the omdb api
Row attributes:
	-movie_id: 
		The movie id that represents a specific movie  
	-director:
		The name of the director 
	-title:
		The title of the movie 
	-imdb_rating: 
		The rating that was given to the movie by imdb 
	-lead_actor: 
		The name of the lead actor of the movie 
	-num_languages: 
		The number of languages in the movie 	

• Tweets Table
Row representation: A specific tweet generated by the twitter api
Row attributes: 
	-id_str: 
		The id number that represents a specific tweet
	-user_id:
		the id number that represents a specific user 
	-tweet_text: 
		The specific tweet itself as seen on twitter 
	-num_retweets: 
		how many times the tweet has been retweeted 
	-num_favs: 
		how many time the tweet has been favorited 
	-actor_search: 
		The name of the actor that was used as a search term to generate the tweet 


• Users Table
Row representation: A specific user on twitter that tweeted a generated tweet 
Row attributes: 
	-user_id_str: 
		The id number assosiated with a specific user
	-screen_name: 
		The twitter screen name of a user 
	-user_num_favs:
		The total number of favoirtes by a user 
	-user_num_followers: 
		The total number of followers a user has 
	-user_location: 
		The location a twitter user entered when they made their profile

Data Manipulation Code: 

What else does the code do: 
After gathering data about the movie and twitter users and tweets and putting them in a data base, the code makes queries about intersections of data and process the data in interesting ways.

How is it useful/ what will it show you:
 It gets the followers to favorites ratio, gets total number of retweets based on different actor searches, puts users in order from most followers to least, and compares number of words in a tweet to retweets of that tweet. This information can be used as is or further processed to gain new information. 

 What should a user expect: 
A user should expect to get movie information and tweet information based on the movies that they insert. The twitter information they recieve will be based on the lead actors of the three movies that they choose. A user will then see three data tables and interesting facts about the attributes of the tweets, tweets users, and movies 

Why did you choose this project: 
I chose this project to be able to find out interesting facts about my favorite movies. I did not know how I was going to incorporate the twitter information, however I found that it suplemented the movie information well and I was able to find out interesting new information. 

Soecific line numbers: 


  - Line(s) on which each of your data gathering functions begin(s): 29, 163, 246
  - Line(s) on which your class definition(s) begin(s): 56
  - Line(s) where your database is created in the program: 121, 207, 287 
  - Line(s) of code that load data into your database: 121-139, 207-225, 287-303
  - Line(s) of code (approx) where your data processing code occurs — 325
  where in the file can we see all the processing techniques you used? 325-384
  -  






















