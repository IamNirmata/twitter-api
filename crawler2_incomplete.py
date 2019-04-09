

#importing predefined libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import pymysql
import numpy as np
import pandas as pd
import re
import datetime
#import TextBlob

# authentication with consumer key and access token from another file "credentials"
# it was easy since all my threads could access the file at same time and its easy to update 




auth = OAuthHandler("X6jKCNf05JrVeNBHqHX00503Y",  "9RHTAfZtCzadM7u4TDzWT00UdmAFQDxwAzCkosAluv9qYh6jhu")
auth.set_access_token("1047999837797605377-D0Kq3yEtHEuegdlas2UtNTfDee1tSu","0iJ0NzWCsnqCLhZpLDweW9zhSdzYBl8iWYMHQlQ0B4x69")

# assigning API authentication
api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=5, retry_delay=8,retry_errors=set([401, 404, 500, 503]))

HOST = "localhost"
USER = ""
PASSWD = "sreenath!erdc"
DATABASE = "twitter_db"
# X-Force in action


# number of requests are capped to 600000
limit = 6000000

# Assigning Default geolocation.
defaultLocation = [-82.146732,38.349819,-81.632622,38.413651]

#hunt-charleston

def place_data(p_ID,country,country_code,full_name,name,place_type,url):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")

    cursor = db.cursor()
    insert_query = "INSERT INTO place (p_ID,country,country_code,full_name,name,place_type,url) VALUES (%s,%s,%s,%s, %s, %s,%s)"
    cursor.execute(insert_query, (p_ID,country,country_code,full_name,name,place_type,url))
    db.commit()
    cursor.close()
    db.close()
    return


def bound_box(c1,c2,place_p_ID,p_type):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")

    cursor = db.cursor()
    insert_query = "INSERT INTO place (c1,c2,place_p_ID,p_type) VALUES (%s,%s,%s,%s)"
    cursor.execute(insert_query, (c1,c2,place_p_ID,p_type))
    db.commit()
    cursor.close()
    db.close()
    return


def attributes(place_p_ID,id,street_address,locality,region,iso3,postal_code,phone,twitter,url):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")

    cursor = db.cursor()
    insert_query = "INSERT INTO place (place_p_ID,id,street_address,locality,region,iso3"\
                    ",postal_code,phone,twitter,url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_query, (place_p_ID,id,street_address,locality,region,iso3,postal_code,phone,twitter,url))
    db.commit()
    cursor.close()
    db.close()
    return

# exporting data in MySQL database 'twitter'.
def tweet_data(id,place_p_ID,u_id, created_at,favorite_count
               ,favorited,filter_level,geo,id_str,in_reply_to_screen_name,in_reply_to_status_id
               ,in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str
               ,lang,retweet_count,retweeted,source,text,timestamp_ms,truncated,possibly_sensitive
               ,withheld_copyright,withheld_countries,withheld_scope,time_stamp):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (id,place_p_ID,u_id, created_at,favorite_count,"\
                   "favorited,filter_level,geo,id_str,in_reply_to_screen_name,in_reply_to_status_id" \
                   ",in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str"\
                   ",lang,retweet_count,retweeted,source,text,timestamp_ms,truncated,possibly_sensitive" \
                   ",withheld_copyright,withheld_countries,time_stamp"\
                   ",withheld_scope) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_query, (id,place_p_ID,u_id, created_at,favorite_count
                ,favorited,filter_level,geo,id_str,in_reply_to_screen_name,in_reply_to_status_id
                ,in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str
                ,lang,retweet_count,retweeted,source,text,timestamp_ms,truncated,possibly_sensitive
                ,withheld_copyright,withheld_countries,withheld_scope,time_stamp))
    db.commit()
    cursor.close()
    db.close()
    return

	#user_data function saves user data in table "user"
def user_data(u_id,tweet_id,contributors_enabled,created_at,default_profile,
              default_profile_image,description,favourites_count,follow_request_sent,
              followers_count,following,friends_count,geo_enabled,id_str,
              is_translator,lang,listed_count,location,name,notifications,
              profile_background_color,profile_background_image_url,
              profile_background_image_url_https,profile_background_tile,
              profile_banner_url,profile_image_url,profile_image_url_https,
              profile_link_color,profile_sidebar_border_color,
              profile_sidebar_fill_color,profile_text_color,profile_use_background_image,
              protected,screen_name,show_all_line_media,
              statuses_count,time_zone,url,utc_offset,
              verified,withheld_countries,withheld_scope,
              flag):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")

    cursor = db.cursor()
    insert_query = "INSERT INTO user(u_id,tweet_id"\
                   ",contributors_enabled,created_at,default_profile" \
                   ",default_profile_image,description,favourites_count,follow_request_sent," \
                   "followers_count,following,friends_count,geo_enabled,id_str,"\
                    "is_translator,lang,listed_count,location,name,notifications,"\
                    "profile_background_color,profile_background_image_url,"\
                    "profile_background_image_url_https,profile_background_tile,"\
                    "profile_banner_url,profile_image_url,profile_image_url_https,"\
                    "profile_link_color,profile_sidebar_border_color,"\
                    "profile_sidebar_fill_color,profile_text_color,profile_use_background_image,"\
                    "protected,screen_name,show_all_line_media,"\
                    "statuses_count,time_zone,url,utc_offset,"\
                    "verified,withheld_countries,withheld_scope,"\
                    "flag ) VALUES (%s,%s,%s,%s, %s,%s,%s,%s"\
                    ", %s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s,"\
                    " %s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s"\
                    ", %s,%s,%s,%s, %s,%s,%s)"

    cursor.execute(insert_query, (u_id,tweet_id,contributors_enabled,created_at,default_profile,
                                    default_profile_image,description,favourites_count,follow_request_sent,
                                    followers_count,following,friends_count,geo_enabled,id_str,
                                    is_translator,lang,listed_count,location,name,notifications,
                                    profile_background_color,profile_background_image_url,
                                    profile_background_image_url_https,profile_background_tile,
                                    profile_banner_url,profile_image_url,profile_image_url_https,
                                    profile_link_color,profile_sidebar_border_color,
                                    profile_sidebar_fill_color,profile_text_color,profile_use_background_image,
                                    protected,screen_name,show_all_line_media,
                                    statuses_count,time_zone,url,utc_offset,
                                    verified,withheld_countries,withheld_scope,
                                    flag))
    db.commit()
    cursor.close()
    db.close()
    return



def coordinates(tweet_id,c1,c2,p_type):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (tweet_id,c1,c2,p_type) VALUES (%s,%s,%s,%s)"
    cursor.execute(insert_query, (tweet_id,c1,c2,p_type))
    db.commit()
    cursor.close()
    db.close()
    return

def contributor(tweet_id,id,id_str,screen_name):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (tweet_id,id,id_str,screen_name) VALUES (%s,%s,%s,%s)"
    cursor.execute(insert_query, (tweet_id,id,id_str,screen_name))
    db.commit()
    cursor.close()
    db.close()
    return

def entities(tweet_id):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (tweet_id) VALUES (%s)"
    cursor.execute(insert_query, (tweet_id))
    db.commit()
    cursor.close()
    db.close()
    return

def user_mentions(entities_tweet_id,id,id_str,screen_name,name,indices):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (entities_tweet_id,id,id_str"\
    ",screen_name,name,indices) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_query, (entities_tweet_id,id,id_str,screen_name,name,indices))
    db.commit()
    cursor.close()
    db.close()
    return

def hashtag(entities_tweet_id,no,indices,text,indices2):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (entities_tweet_id,no,indices"\
    ",text,indices2) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(insert_query, (entities_tweet_id,no,indices,text,indices2))
    db.commit()
    cursor.close()
    db.close()
    return

def symbol(entities_tweet_id,text,indices):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (entities_tweet_id,text,indices) VALUES (%s,%s,%s)"
    cursor.execute(insert_query, (entities_tweet_id,text,indices))
    db.commit()
    cursor.close()
    db.close()
    return

def urls(url,user_u_id,user_tweet_id):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (url,user_u_id,user_tweet_id) VALUES (%s,%s,%s)"
    cursor.execute(insert_query, (url,user_u_id,user_tweet_id))
    db.commit()
    cursor.close()
    db.close()
    return

def url(urls_url,urls_user_u_id,urls_user_tweet_id,expanded_url,indices,display_url):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (urls_url,urls_user_u_id,urls_user_tweet_id"\
                   ",expended_url,indices,display_url) VALUES (%s,%s,%s,%s,%s,%s)"
    cursor.execute(insert_query, (urls_url,urls_user_u_id,urls_user_tweet_id,expanded_url,indices,display_url))
    db.commit()
    cursor.close()
    db.close()
    return



def media(m_id,entities_tweet_id,id_str,media_url,media_url_https,url,display_url,expanded_url,source_status_id,source_status_is_str
            ,type,indices,resize,title,description,embeddable,monetizable):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (m_id,entities_tweet_id,id_str,media_url,media_url_https,url,display_url,expanded_url"\
                                      ",source_status_id,source_status_is_strtype,indices,resize,title"\
                                      ",description,embeddable,monetizable) VALUES (%s,%s,%s,%s"\
                                          ", %s,%s,%s,%s, %s,%s,%s,%s, %s,%s,%s,%s, %s)"
    cursor.execute(insert_query, (m_id,entities_tweet_id,id_str,media_url,media_url_https,url,display_url,
                                    expanded_url,source_status_id,source_status_is_str
                                    ,type,indices,resize,title,description,embeddable,monetizable))
    db.commit()
    cursor.close()
    db.close()
    return




def size(media_m_id,media_entities_tweet_id):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (media_m_id,media_entities_tweet_id) VALUES (%s,%s)"
    cursor.execute(insert_query, (media_m_id,media_entities_tweet_id))
    db.commit()
    cursor.close()
    db.close()
    return



def small(w,h,resize,size_media_m_id):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (w,h,resize,size_media_m_id) VALUES (%s,%s,%s,%s,)"
    cursor.execute(insert_query, (w,h,resize,size_media_m_id))
    db.commit()
    cursor.close()
    db.close()
    return

def medium(w,h,resize,size_media_m_id):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (w,h,resize,size_media_m_id) VALUES (%s,%s,%s,%s)"
    cursor.execute(insert_query, (w,h,resize,size_media_m_id))
    db.commit()
    cursor.close()
    db.close()
    return


def large(w,h,resize,size_media_m_id):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (w,h,resize,size_media_m_id) VALUES (%s,%s,%s,%s)"
    cursor.execute(insert_query, (w,h,resize,size_media_m_id))
    db.commit()
    cursor.close()
    db.close()
    return


def thumb(w,h,resize,size_media_m_id):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (w,h,resize,size_media_m_id) VALUES (%s,%s,%s,%s)"
    cursor.execute(insert_query, (w,h,resize,size_media_m_id))
    db.commit()
    cursor.close()
    db.close()
    return




# overriding and customizing tweepy.StreamListener class
class MyStreamListener(StreamListener):

    # initializing function in __init__
    def __init__(self, api=None):
        # Opening file to append data
        self.saveFile = open(fileName, 'a')
        # Counting limitation
        self.count = 0
        super(MyStreamListener, self).__init__()

    # Writing data to the file in JSON format
    def on_data(self, data):

        # Write the data to the file in JSON format

        self.saveFile.write(data)
        print(self.count + 1)
        # Loads the data in JSON format to use like dictionary
        dictData = json.loads(data)
        try:
            print("ID: " + str(dictData["id"]))
            print(dictData["created_at"])
            print("text:" + dictData["text"])
           

            print("\n")
            
                ##########################################################
            p_ID= str(dictData["place"]["id"])
            country= str(dictData["place"]["country"])
            country_code= str(dictData["place"]["country_code"])
            full_name= str(dictData["place"]["full_name"])
            name= str(dictData["place"]["name"])
            place_type= str(dictData["place"]["place_type"])
            url= str(dictData["place"]["url"])

            place_data(p_ID,country,country_code,full_name,name,place_type,url)
                ###########################################################
            c1= str(dictData["place"]["bound_box[[0]]"])
            c2= str(dictData["place"]["bound_box[[2]]"])
            place_p_ID=str(dictData["place"]["id"])
            p_type=str(dictData["place"]["bound_box"]["type"])
            
            bound_box(c1,c2,place_p_ID,p_type)

                ##########################################################
			place_p_ID=str(dictData["place"]["id"])
            id=str(dictData["place"]["attributes"]["id"])
            street_address=str(dictData["place"]["attributes"]["street_address"])
            locality=str(dictData["place"]["attributes"]["locality"])
            region=str(dictData["place"]["attributes"]["region"])
            iso3=str(dictData["place"]["attributes"]["iso3"])
            postal_code=str(dictData["place"]["attributes"]["postal_code"])
            phone=str(dictData["place"]["attributes"]["phone"])
            twitter=str(dictData["place"]["attributes"]["twitter"])
            url=str(dictData["place"]["attributes"]["url"])
            
            attributes(place_p_ID,id,street_address,locality,region,iso3,postal_code,phone,twitter,url)
                ##########################################################




            #mapping with key-value pair method
            # grab the wanted data from the Tweet
            id = (dictData["id"])
            place_p_ID=str(dictData["place"]["id"])
            u_id = str(dictData["user"]["id"])
            created_at = (dictData["created_at"])
            favorite_count = (dictData["favorite_count"])
            favorited=str(dictData["favoriteD"])
            filter_level=str(dictData["filter_level"])
            geo=str(dictData["geo"])
            id_str=str(dictData["favoriteD"])
            in_reply_to_screen_name=str(dictData["in_reply_to_screen_name"])
            in_reply_to_status_id=
            in_reply_to_status_id_str=
            retweet_count = (dictData["retweet_count"])

           
            
            in_reply_to_user_id = dictData["in_reply_to_user_id"]
            in_reply_to_user_id_str = str(dictData["in_reply_to_user_id_str"])
            lang=str(dictData["lang"])
            retweet_count=str(dictData["retweet_count"])
            retweeted=str(dictData["retweeted"])
            source=str(dictData["source"])
            text=str(dictData["text"])
            timestamp_ms=str(dictData["timestamp_ms"])
            truncated=str(dictData["truncated"])
            possibly_sensitive=str(dictData["possibly_sensitive"])
            withheld_copyright=str(dictData["withheld_copyright"])
            withheld_countries=str(dictData["withheld_countries"])
            withheld_scope=str(dictData["withheld_scope"])
            time_stamp=str(datetime.datetime.now())

            tweet_data(id,place_p_ID,u_id, created_at,favorite_count
               , favorited,filter_level,geo,id_str,in_reply_to_screen_name,in_reply_to_status_id
               ,in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str
               ,lang,retweet_count,retweeted,source,text,timestamp_ms,truncated,possibly_sensitive
               ,withheld_copyright,withheld_countries,withheld_scope,time_stamp):
                ########################################################################
            # user data
            

            u_id = str(dictData["user"]["id"])
            tweet_id=(dictData["id"])
            contributors_enabled=str(dictData["user"]["contributors_enabled"])
            created_at=str(dictData["user"]["created_at"])
            default_profile=str(dictData["user"]["default_profile"])
            default_profile_image=str(dictData["user"]["default_profile_image"])
            description=str(dictData["user"]["description"])
            favorite_count=str(dictData["user"]["favorite_count"])
            follow_request_sent=str(dictData["user"]["follow_request_sent"])
            followers_count=str(dictData["user"]["followers_count"])
            following=str(dictData["user"]["following"])
            friends_count=str(dictData["user"]["friends_count"])
            geo_enabled=str(dictData["user"]["geo_enabled"])
            id_str = str(dictData["user"]["id_str"])
            is_translator=str(dictData["user"]["is_translator"])
            lang = str(dictData["user"]["lang"])


            listed_count = str(dictData["user"]["listed_count"])
            location = str(dictData["user"]["location"])
            name = str(dictData["user"]["name"])
            notifications = str(dictData["user"]["notifications"])
            profile_background_color=str(dictData["user"]["profile_background_color"])

            profile_background_image_url = str(dictData["user"]["profile_background_image_url"])
            profile_background_image_url_https = str(dictData["user"]["profile_background_image_url_https"])
            profile_background_tile = str(dictData["user"]["profile_background_tile"])
            profile_banner_url = str(dictData["user"]["profile_banner_url"])
            profile_image_url = str(dictData["user"]["profile_image_url"])
            profile_image_url_https = str(dictData["user"]["profile_image_url_https"])
            profile_link_color = str(dictData["user"]["profile_link_color"])
            profile_sidebar_border_color = str(dictData["user"]["profile_sidebar_border_color"])
            profile_sidebar_fill_color = str(dictData["user"]["profile_sidebar_fill_color"])
            profile_text_color = str(dictData["user"]["profile_text_color"])
            profile_use_background_image = str(dictData["user"]["profile_use_background_image"])
            protected = str(dictData["user"]["protected"])
            screen_name = str(dictData["user"]["screen_name"])
            show_all_line_media= str(dictData["user"]["show_all_line_media"])
            statuses_count== str(dictData["user"]["statuses_count"])
            time_zone = str(dictData["user"]["time_zone"])
            url = str(dictData["user"]["url"])
            utc_offset = str(dictData["user"]["utc_offset"])
            verified = str(dictData["user"]["verified"])
            withheld_countries= str(dictData["user"]["withheld_countries"])
            withheld_scope= str(dictData["user"]["withheld_scope"])
            flag=0
            
            user_data(u_id,tweet_id,contributors_enabled,created_at,default_profile,
              default_profile_image,description,favourites_count,follow_request_sent,
              followers_count,following,friends_count,geo_enabled,id_str,
              is_translator,lang,listed_count,location,name,notifications,
              profile_background_color,profile_background_image_url,
              profile_background_image_url_https,profile_background_tile,
              profile_banner_url,profile_image_url,profile_image_url_https,
              profile_link_color,profile_sidebar_border_color,
              profile_sidebar_fill_color,profile_text_color,profile_use_background_image,
              protected,screen_name,show_all_line_media,
              statuses_count,time_zone,url,utc_offset,
              verified,withheld_countries,withheld_scope,
              flag)

                ####################################################
			
            

            

            # print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
			
			
			
			#calling out all db connection functions (place_data,user_data,store_data) to store data in DB
            # insert the data into the MySQL database
            

            # insert user data into the MySQL database
            

            # data about place
            

		#baseexception to show what type of the error just in case
        except BaseException as e:
            print("Error on_data %s" % str(e))

        self.count += 1
        if (self.count >= limit):
            # Closing the file when the requests go beyond the limitation
            self.saveFile.close()
            return False
			#saving raw JSON format data (i did this to help myself with mapping so that i can look into the data and find out whats coming and what not
			
    def on_error(self, status):
        if (status == 420):
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)
        
        
class TweetAnalyzer():
    
    
    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df
    
    
   


# Changing file name to save tweets in JSON format that searched by location
fileName = 'tweetsByLocations.json'

# Opening file to overwrite
saveFile = open(fileName, 'w')
# closing file
saveFile.close()




		
print("\nCollecting tweets that originated from the geographic region around " + str(defaultLocation) + "\n")
# Stream tweets that filter by the geolocation that the user put in
tweepy.Stream(auth=api.auth, listener=MyStreamListener()).filter(locations=defaultLocation)



