import  json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream



# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="Zt3go661AoG8AeKFY6KXvEOkJ"
consumer_secret="hA4mb3evaPseuC9ThdeDmxk6sIkoUnoXQIkbuHyPw3R8pu9t39"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="156953790-Gu5ccWKt4Avq61fUKwu23P6i66XKDnZG1lGNIKTE"
access_token_secret="oi7urRGg1leo4uJWLv86BL4VyZP4c3ZI4JpLtyBEWQiNI"


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is tweets_counta basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        print(data.rstrip())
        return True

    def on_exception(self, exception):
        print(exception)
        return

    def on_error(self, status):
        print(status)

    def on_status(self, status):
        return

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
   # msg = raw_input('Enter search string? ')
    #query=("[\'"+msg+"\']")
    #print(query)
    stream.filter(track=['trump'], stall_warnings=True)

