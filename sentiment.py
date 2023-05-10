
# Demonstrates connecting to the twitter API and accessing the twitter stream

import twitter
import json
import sys
import codecs

# Go to http://developer.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://developer.twitter.com/docs/auth/oauth for more information
# on Twitter's OAuth implementation.

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
print('Establish Authentication Credentials')

CONSUMER_KEY = 'flXF7aYHDhzQsI8WQeqX0hLZT'
CONSUMER_SECRET = 'ehVewUjbNQUqjGjMKzEzXB39OqyyNsxlgc2Ovb36nk7lPS8lF6'
ACCESS_TOKEN = '3024475278-y5DruH8bdxNgTWUgR8fhYxAgANVE3BsI78z7aTh'
ACCESS_TOKEN_SECRET = 'gzxWtIACQzoQtOQ0nICLdzPP2Zw3EoGxZ4BvZl8G6mOTD'


auth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

print("Nothing to see by displaying twitter_api")
print(" except that it's now a defined variable")
print()
print(twitter_api)
print()

# Begin the search
q = input('Enter your first search term: ')
q1 = input('Enter your second search term: ')
count = 1000

search_results = twitter_api.search.tweets(q=q, count=count)

statuses = search_results['statuses']

for _ in range(5):
    try:
        next_results = search_results['search_metadata']['next_results']
    # except KeyError, e:  # No more results when next_results doesn't exist
    except KeyError:
        break

    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    kwargs = dict([kv.split('=') for kv in next_results[1:].split("&")])

    search_results = twitter_api.search.tweets(**kwargs)
    statuses += search_results['statuses']

status_texts = [status['text']
                for status in statuses]

screen_names = [user_mention['screen_name']
                for status in statuses
                for user_mention in status['entities']['user_mentions']]

hashtags = [hashtag['text']
            for status in statuses
            for hashtag in status['entities']['hashtags']]

# Compute a collection of all words from all tweets
words = [w
         for t in status_texts
         for w in t.split()]

sent_file = open('AFINN-111.txt')

scores = {}  # initialize an empty dictionary
for line in sent_file:
    term, score = line.split("\t")
    # The file is tab-delimited.
    # "\t" means "tab character"
    scores[term] = int(score)  # Convert the score to an integer.

score = 0
for word in words:
    uword = word.encode('utf-8')
    if word in scores.keys():
        score = score + scores[word]
print("Score 1: "+str(score))

# Bein second search

search_results1 = twitter_api.search.tweets(q=q1, count=count)

statuses1 = search_results1['statuses']

for _ in range(5):
    try:
        next_results1 = search_results1['search_metadata']['next_results']
    # except KeyError, e:  # No more results when next_results doesn't exist
    except KeyError:
        break

    # Create a dictionary from next_results, which has the following form:
    # ?max_id=313519052523986943&q=NCAA&include_entities=1
    kwargs1 = dict([kv.split('=') for kv in next_results1[1:].split("&")])

    search_results1 = twitter_api.search.tweets(**kwargs1)
    statuses1 += search_results1['statuses']

status_texts1 = [status['text']
                 for status in statuses1]

screen_names1 = [user_mention['screen_name']
                 for status in statuses1
                 for user_mention in status['entities']['user_mentions']]

hashtags1 = [hashtag['text']
             for status in statuses1
             for hashtag in status['entities']['hashtags']]

# Compute a collection of all words from all tweets
words1 = [w1
          for t1 in status_texts1
          for w1 in t1.split()]


score1 = 0
for word1 in words1:
    uword = word1.encode('utf-8')
    if word1 in scores.keys():
        score1 = score1 + scores[word1]
print("Score 2: "+str(score1))


if score >= score1:
    print(q + " had a higher sentiment score.")
    winningWords = words
    winningScreenNames = screen_names
    winningHashtags = hashtags
    winningStatusTexts = status_texts
    winningStatuses = statuses
else:
    print(q1 + " had a higher sentiment score.")
    winningWords = words1
    winningScreenNames = screen_names1
    winningHashtags = hashtags1
    winningStatusTexts = status_texts1
    winningStatuses = statuses1

# Explore the first 5 items for each...

print(json.dumps(winningStatusTexts[0:5], indent=1))
print(json.dumps(winningScreenNames[0:5], indent=1))
print(json.dumps(winningHashtags[0:5], indent=1))
print(json.dumps(winningWords[0:5], indent=1))


# A function for computing lexical diversity
def lexical_diversity(tokens):
    return 1.0*len(set(tokens))/len(tokens)


# A function for computing the average number of words per tweet
def average_words(statuses):
    total_words = sum([len(s.split()) for s in statuses])
    return 1.0*total_words/len(statuses)


print('Lexical diversity of words: ')
print(lexical_diversity(winningWords))
print('Lexical diversity of screen names: ')
print(lexical_diversity(winningScreenNames))
print('Lexical diversity of hashtags: ')
print(lexical_diversity(winningHashtags))
print('Average number of words per tweet: ')
print(average_words(winningStatusTexts))
