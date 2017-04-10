## Your name:
## The option you've chosen: 2

# Put import statements you expect to need here!
import unittest
import itertools
import collections
import tweepy
import json
import sqlite3
import re 
from pprint import pprint
















# Write your test cases here.
class OMDB_tests(unittest.TestCase): 
	def test_1(self):
		x = movies(star_wars_info_dic)
		self.assertEqual(x.get_director(),'George Lucas')
	def test_2(self): 
		x = movies(star_wars_info_dic)
		self.assertEqual(x.year_released(), 1977) 
	def test_3(self): 
		x = movies(star_wars_info_dic)
		y = x.get_all_movie_data()
		self.assertEqual(type(y), tuple)
	def test_4(self): 
		x = movies(star_wars_info_dic)
		self.assertEqual(x.leading_actor, 'Mark Hamill')

class twitter_tests(unittest.TestCase):		
	def test_5(self):
		x = twitter_user('Mark Hamill')
		y = x.get_num_followers
		self.assertEqual(y, 1740000)	
	def test_6(self): 
		x = twitter_user('Mark Hamill')
		y = x.get_user_id()
		self.assertEqual(type(y), int)
	def test_7(self): 
		x = twitter_user('Mark Hamill')
		y = x.num_favs()
		self.assertEqual(type(y), int)
	def test_8(self): 
		x = twitter_user('Mark Hamill')
		y = x.get_location()
		self.assertEqual(type(y), str)

		






unittest.main(verbosity=2)

## Remember to invoke all your tests...