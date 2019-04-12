import sys
import time
from pyspark import SparkContext
from pyspark.streaming import  StreamingContext
from pyspark.sql import  SQLContext
import json
import re
import  Algorithmia
from itertools import chain
from textblob import TextBlob
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math
import spacy
import operator
import  os
opinionCount = 0
totalCount = 0
opininMAX =0
totalMAX =0
nlp = spacy.load('en')

from collections import namedtuple

TagCount = namedtuple('TagCount', ("VulText","VulCount","OpText","OpCount"))

def clean_tweet(text):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ",text).split())

def removeStopWords(jsonTweetsText):
    sys.setrecursionlimit(10000)
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(jsonTweetsText)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence

def extractTweetText(tweetJSON):
    if ('text' in tweetJSON):
        jsonTweetsText =clean_tweet(tweetJSON['text'])
        #tweetsText = removeStopWords(jsonTweetsText)
        return jsonTweetsText
    else:
        return ''

def ratioOfTweetsContainingOpinion(text):
    global opinionCount
    global totalCount
    text_tweet = [textQ for textQ in text.split(" ")]
    #print(text_tweet)
    totalCount = 1
    for word in text_tweet :
        #print("*********"+ word)
        if word in ["think", "thought", "thinks", "thinking", "knowing", "knew", "knows", "know", "considering","considers", "considered", "consider"]:
            #print("************"+ str(opinionCount))
            opinionCount = 1
            break
        else:
            opinionCount = 0
    return ("opnionCount",opinionCount,totalCount)

def ratioOfTweetsContainingTentative(text):
    text_tweet = [textQ for textQ in text.split(" ")]
    tentativeCount = 0
    for word in text_tweet:
        if word in ["maybe", "guess", "perhaps", "experimental" , "experiment" , ]:
            tentativeCount = 1
            break
        else:
            tentativeCount = 0

	return ("tentativeCount",tentativeCount)



def presenceOfVulgarity(text):
    text_tweet = [textQ for textQ in text.split(" ")]
    for word in text_tweet:
        if word in ["2g1c", "acrotomophilia", "anal", "anilingus", "anus", "arsehole", "ass", "asshole", "assmunch", "erotic", "autoerotic", "babeland","barenaked", "bastardo", "bastinado", "bbw", "bdsm", "beaver cleaver", "beaver lips", "bestiality", "bi curious", "big black", "big breasts", "big knockers", "big tits", "bimbos", "birdlock", "bitch", "blumpkin", "bollocks", "bondage", "boner", "boob", "boobs", "booty", "bukkake", "bulldyke", "bullet", "bung", "bunghole", "busty", "butt", "buttcheeks", "butthole", "camel", "camgirl", "camslut", "camwhore", "carpet", "carpetmuncher", "clit", "clitoris", "clover clamps", "clusterfuck", "cock", "cocks", "coprolagnia", "coprophilia", "cornhole", "cum", "cumming", "cunnilingus", "cunt", "darkie", "daterape", "deepthroat", "dick", "dildo", "dirty pillows", "dirty sanchez", "dog style", "doggie style", "doggiestyle", "doggy style", "doggystyle", "dolcett", "domination", "dominatrix", "dommes", "donkey punch", "double dong", "double penetration", "dp action", "eat my ass", "ecchi", "ejaculation", "erotic", "erotism", "escort", "ethical slut", "eunuch", "faggot", "fecal", "felch", "fellatio", "feltch", "female squirting", "femdom", "figging", "fingering", "fisting", "foot fetish", "footjob", "frotting", "fuck", "fucking", "fuck buttons", "fudge packer", "fudgepacker", "futanari", "g-spot", "gang bang", "gay sex", "genitals", "giant cock", "girl on", "girl on top", "girls gone wild", "goatcx", "goatse", "gokkun", "golden shower", "goo girl", "goodpoop", "goregasm", "grope", "group sex", "guro", "hand job", "handjob", "hard core", "hardcore", "hentai", "homoerotic", "honkey", "hooker", "hot chick", "how to kill", "how to murder", "huge fat", "humping", "incest", "intercourse", "jack off", "jail bait", "jailbait", "jerk off", "jigaboo", "jiggaboo", "jiggerboo", "jizz", "juggs", "kike", "kinbaku", "kinkster", "kinky", "knobbing", "leather restraint", "masturbate","motherfucker", "muffdiving", "nambla", "nawashi", "negro", "neonazi", "nig nog", "nigga", "nigger", "nimphomania", "nipple", "nipples", "nude", "nudity", "nympho", "nymphomania", "octopussy", "omorashi", "orgasm", "orgy", "paedophile", "panties", "panty", "pedobear", "pedophile", "pegging", "penis", "pissing", "pisspig", "playboy",  "ponyplay", "poof", "poop chute", "poopchute", "porn", "porno", "pornography", "pubes", "pussy", "rimming", "rosy palm", "s&m", "sadism", "scat", "schlong", "scissoring", "semen", "sex", "sexo", "sexy", "shemale", "shibari", "shit", "shota", "shrimping", "slanteye", "slut", "smut", "snatch", "snowballing", "sodomize", "sodomy", "spic", "spooge", "spread legs", "strap on", "strapon", "strappado","suck", "sucks", "suicide", "sultry",  "tit", "tits", "titties", "titty", "tushy", "twat", "twink", "twinkie","undressing", "xx", "xxx", "yaoi", "yellow showers", "yiffy", "zoophilia"]:
            vulgarityCount = 1
        else:
            vulgarityCount = 0
	return ("vulgarityCount",vulgarityCount)


def get_tweet_sentiment_Pos(text):

    analysis = TextBlob(text)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return ("Positive",1)
    else:
        return ("Positive",0)



def get_tweet_sentiment_Neu(text):

    analysis = TextBlob(text)
    # set sentiment
    if analysis.sentiment.polarity == 0:
        return ("Neutral",1)
    else:
        return ("Neutral",0)

def get_tweet_sentiment_Neg(text):

    analysis = TextBlob(text)
    # set sentiment
    if analysis.sentiment.polarity < 0:
        return ("Negative",1)
    else:
        return ("Negative",0)


if __name__ == '__main__':
    path= os.environ['HOME']
    batchInterval = 1
    windowLegnth = 15 * batchInterval
    sc = SparkContext(appName= "ABC")
    ssc = StreamingContext(sc, batchInterval)
    sqlContext = SQLContext(sc)
    tweetsDStream = ssc.socketTextStream(sys.argv[1], int(sys.argv[2]))
    tweetRDD = tweetsDStream.map(lambda tweet: extractTweetText(json.loads(tweet)))
    words = tweetRDD.map(lambda text:[ratioOfTweetsContainingTentative(text),presenceOfVulgarity(text),ratioOfTweetsContainingOpinion(text),get_tweet_sentiment_Pos(text),get_tweet_sentiment_Neu(text),get_tweet_sentiment_Neg(text)])
    countWords= words.map(lambda x : list(chain.from_iterable(x)))
    countWords.map(lambda  x : (x[1],x[3],x[5],x[6],x[8],x[10],x[12])).saveAsTextFiles(path+"/text.txt")
    #col.union()map(lambda x : ).saveAsTextFiles("/Users/abhaymone/Documents/text.txt")
    #countWords.saveAsTextFiles()
    #countWords.foreachRDD(lambda rdd: rdd.toDF().registerTempTable("TempTable"))
    ssc.start()
    #sqlContext = SQLContext(sc)
    #count = 0
    #while count <  100 :
    #    time.sleep(15)
    #   count = count + 1
    #    textTwitter = sqlContext.sql('select SUM(VulCount),SUM(OpCount) from TempTable group by VulText, VulCount')
    #    for row in textTwitter.collect():
    #        print(row['SUM(VulCount)'], row['SUM(OpCount)'])
    ssc.awaitTermination(batchInterval * 5 * 1000)

