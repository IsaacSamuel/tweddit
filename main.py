import praw
import tweepy, time, sys
import configparser
import re



#Parses reddit comment to check if it references a twitter handle
def references_twitter_handle(comment):

	if comment.body is not None:
		if "twitter" or "Twitter" or "Tweddit" or "tweddit" in comment.body:
			#Uses regular expressions to search for a twitter handle
			return re.findall("(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9]+)", comment.body)

	return []

def twitter_reply(handle, permalink, comment_text):
	retval = 'Hey @' + handle  + ', you may have been mentioned on reddit. '

	count = 0;
	if len(retval) + len(permalink) < 120:
		retval += '"'
		while len(retval) + permalink < 135:
			retval += comment_text[count]
			count += 1

		retval += '..." '

	retval += permalink
	return retval

def reddit_reply(twitter_handle, tweet_url):
	retval = "Hey, I noticed you mentioned the valid twitter handle " + twitter_handle + ". I went ahead and sent them a tweet that will link them to this post. https://twitter.com/tweddit_bot/status/" + tweet_url
	retval += "\n\n*I am a bot that tries to bridge the gap between Twitter and Reddit. If you reference me or Twitter and a valid Twitter handle in your post, I tweet the post to the twitter handle in question.*"
	return retval



#searches reddit for posts that appear to reference twitter handles, tweets them out.
def reddit_stream(twitter_api, reddit):

	for comment in reddit.subreddit('all').stream.comments():
		if ((comment.id not in already_done)) :

			twitter_handle = references_twitter_handle(comment)

			if len(twitter_handle) != 0:
				print(twitter_handle)

				print comment.body

				try :
					user = twitter_api.get_user(twitter_handle[0])

					tweet = twitter_reply(twitter_handle[0], "reddit.com" + str(comment.permalink()), comment.body)

					#Tweets out reddit link, returns object of that status
					status_object = twitter_api.update_status(tweet)
					tweet_id = status_object.id



					reply_text = reddit_reply(twitter_handle[0], str(tweet_id))
					comment.reply(reply_text)

					with open("test.txt", "a+") as file:
						file.write(tweet + "\n")
						file.write(reply + "\n\n")


						
				except:
					print("User not found.\n")


				already_done.add(comment.id)


	#post any responses to twitter comments








already_done = set()

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
twitter_api = tweepy.API(tweepy_auth)

#This sets up the reddit api
reddit = praw.Reddit('tweddit')

reddit_stream(twitter_api, reddit)