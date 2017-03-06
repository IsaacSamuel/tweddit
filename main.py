import praw
import tweepy, time, sys
import configparser
import re



#Parses reddit comment to check if it references a twitter handle
def references_twitter_handle(comment):
	if comment.body is not None:
		return re.findall("(?<=^|(?<=[^a-zA-Z0-9-_\\.]))@([A-Za-z]+[A-Za-z0-9_]+)", comment.body)

	else:
		return []


def run():
	#Praw, the reddit engine, automatically reads all your authorization stuff from your praw.ini file
	#Tweepy, on the other hand, requires you to read in everything manually.
	#This pulls the variables from .ini
	config = configparser.ConfigParser()
	config.read("tweepy.ini")
	tweepy_consumer_key =  config.get("tweepy", "CONSUMER_KEY")
	tweepy_consumer_secret = config.get("tweepy", "CONSUMER_SECRET")
	tweepy_access_key = config.get("tweepy", "ACCESS_KEY")
	tweepy_access_secret = config.get("tweepy", "ACCESS_SECRET")

	#This sets up the twitter api
	tweepy_auth = tweepy.OAuthHandler(tweepy_consumer_key, tweepy_consumer_secret)
	tweepy_auth.set_access_token(tweepy_access_key, tweepy_access_secret)
	api = tweepy.API(tweepy_auth)

	#This sets up the reddit api
	reddit = praw.Reddit('tweddit')


	for comment in reddit.subreddit('all').stream.comments():
		if ((comment.id not in already_done)) :

			twitter_handle = references_twitter_handle(comment)

			if len(twitter_handle) != 0:
				print(twitter_handle)

				print comment.body
				#create twitter reply

				#link to twitter reply on reddit

				already_done.add(comment.id)


	#post any responses to twitter comments

	time.sleep(20)
	run()


already_done = set()
run()