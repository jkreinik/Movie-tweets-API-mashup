## Your name:
## The option you've chosen: 2

# Put import statements you expect to need here!
import unittest
import itertools
import collections
import tweepy
import twitter_info # same deal as always...
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
		



	unittest.main(verbosity=2)

## Remember to invoke all your tests...