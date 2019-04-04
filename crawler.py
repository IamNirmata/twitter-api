# X-Force in action


#importing predefined libraries
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import json
import pymysql

# authentication with consumer key and access token from another file "credentials"
# it was easy since all my threads could access the file at same time and its easy to update 
import credentials



auth = OAuthHandler(credentials.CONSUMER_KEY, credentials.CONSUMER_SECRET)
auth.set_access_token(credentials.ACCESS_TOKEN, credentials.ACCESS_TOKEN_SECRET)

# assigning API authentication
api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=5, retry_delay=8,retry_errors=set([401, 404, 500, 503]))

# connecting to MySQL server
HOST = "10.103.92.251"
USER = "sreenath"
PASSWD = "sreenath!erdc"
DATABASE = "smart_gate"

# number of requests are capped to 600000
limit = 6000001

# Assigning Default geolocation.
defaultLocation = [-74.4057,40.0583,-74.0060,40.7128]
#nyc 40.7128° N, 74.0060° W
#NJ 40.0583° N, 74.4057° W
#california 36.7783° N, 119.4179° W


# Function that get input geolocation from the user
def inputLocations():
    locations = list()  # Set locations to empty list
    # loading longitude of the left point
    locations.append(float(input("Enter the left Longitude location  " + str(i + 1) + " value:")))
    # loading latitude of the left point
    locations.append(float(input("Enter the left Latitude location  " + str(i + 1) + "  value:")))
    # loading longitude of the right point
    locations.append(float(input("Enter the right Longitude location " + str(i + 1) + "  value:")))
    # loading latitude of the right point
    locations.append(float(input("Enter the right Latitude location  " + str(i + 1) + "  value:")))
    return locations


# exporting data in MySQL database 'twitter'.
def store_data(id, created_at, text, id_str, favorited, retweet_count, favorite_count, source
               , in_reply_to_status_id, in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str
               , in_reply_to_screen_name):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")
	#establishing connection to database
    cursor = db.cursor()
    insert_query = "INSERT INTO tweet (id,created_at, text,id_str,favorited,retweet_count,favorite_count,source" \
                   ",in_reply_to_status_id,in_reply_to_status_id_str,in_reply_to_user_id,in_reply_to_user_id_str" \
                   ",in_reply_to_screen_name) VALUES (%s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s)"
    cursor.execute(insert_query, (id, created_at, text, id_str, favorited, retweet_count, favorite_count, source
                                  , in_reply_to_status_id, in_reply_to_status_id_str, in_reply_to_user_id,
                                  in_reply_to_user_id_str
                                  , in_reply_to_screen_name))
    db.commit()
    cursor.close()
    db.close()
    return

	#user_data function saves user data in table "user"
def user_data(u_id, id_str, lang,
              listed_count,
              location,
              name,
              profile_background_image_url,
              profile_background_image_url_https,
              profile_background_tile,
              profile_image_url,
              profile_image_url_https,
              profile_sidebar_border_color,
              profile_sidebar_fill_color,
              profile_text_color,
              profile_use_background_image,
              protected,
              screen_name,
              url,
              utc_offset,
              verified,
              statuses_count, time_zone, tweet_id, contributors_enabled):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")

    cursor = db.cursor()
    insert_query = "INSERT INTO user(u_id,id_str,lang,listed_count,location,name,profile_background_image_url,profile_background_image_url_https" \
                   ",profile_background_tile,profile_image_url,profile_image_url_https,profile_sidebar_border_color,profile_sidebar_fill_color,profile_text_color,profile_use_background_image" \
                   ",protected,screen_name,url, utc_offset,verified,statuses_count,time_zone,tweet_id,contributors_enabled) VALUES (%s,%s,%s,%s, %s, %s,%s,%s,%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    cursor.execute(insert_query, (u_id, id_str, lang, listed_count, location, name, profile_background_image_url,
                                  profile_background_image_url_https,
                                  profile_background_tile,
                                  profile_image_url,
                                  profile_image_url_https,
                                  profile_sidebar_border_color,
                                  profile_sidebar_fill_color,
                                  profile_text_color,
                                  profile_use_background_image,
                                  protected,
                                  screen_name,
                                  url,
                                  utc_offset,
                                  verified,
                                  statuses_count, time_zone, tweet_id, contributors_enabled))
    db.commit()
    cursor.close()
    db.close()
    return

	#saves data about the place in table "place"
def place_data(place_type, country_code, full_name, p_id, p_name, p_url, tweet_id):
    db = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8mb4")

    cursor = db.cursor()
    insert_query = "INSERT INTO place (place_type,country_code,full_name,p_id,p_name,p_url,tweet_id) VALUES (%s,%s,%s,%s, %s, %s,%s)"
    cursor.execute(insert_query, (place_type, country_code, full_name, p_id, p_name, p_url, tweet_id))
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
            print("ID_str:" + str(dictData["id_str"]))
            print("favorited:" + str(dictData["favorited"]))
            print("filter_level:" + dictData["filter_level"])
            print("retweet_count:" + str(dictData["retweet_count"]))
            print("favorite_count:" + str(dictData["favorite_count"]))
            print("source:" + str(dictData["source"]))
            print("truncated:" + str(dictData["truncated"]))
            print("in_reply_to_status_id:" + str(dictData["in_reply_to_status_id"]))
            print("in_reply_to_status_id_str:" + str(dictData["in_reply_to_status_id_str"]))
            print("in_reply_to_user_id:" + str(dictData["in_reply_to_user_id"]))
            print("in_reply_to_user_id_str:" + str(dictData["in_reply_to_user_id_str"]))
            print("in_reply_to_screen_name:" + str(dictData["in_reply_to_screen_name"]))

            print("contributors_enabled:" + str(dictData["user"]["contributors_enabled"]))
            print("created_at:" + str(dictData["user"]["created_at"]))
            print("default_profile:" + str(dictData["user"]["default_profile"]))
            print("default_profile_image:" + str(dictData["user"]["default_profile_image"]))
            print("favourites_count:" + str(dictData["user"]["favourites_count"]))
            print("follow_request_sent:" + str(dictData["user"]["follow_request_sent"]))
            print("followers_count:" + str(dictData["user"]["followers_count"]))
            print("location:" + str(dictData["user"]["location"]))
            print("location:" + str(dictData["user"]["location"]))
            print("location:" + str(dictData["user"]["location"]))
            print("location:" + str(dictData["user"]["location"]))
            print("location:" + str(dictData["user"]["location"]))

            """
            #print("url:" + str(dictData["url"]))
            #print("description:" + dictData["description"])
            #print("translator_type:" + dictData["translator_type"])

			print("protected:" + dictData["protected"])
            print("verified:" + dictData["verified"])
            print("followers_count:" + str(dictData["followers_count"]))
            print("friends_count:" + str(dictData["friends_count"]))
            print("listed_count:" + str(dictData["listed_count"]))
            print("statuses_count:" + str(dictData["statuses_count"]))
            print("utc_offset:" + dictData["utc_offset"])
            print("time_zone:" + dictData["time_zone"])
            print("lang:" + dictData["lang"])
            print("geo_enabled:" + dictData["geo_enabled"])
            print("contributors_enabled:" + dictData["contributors_enabled"])
            print("is_translator:" + dictData["is_translator"])
            print("profile_background_color:" + dictData["profile_background_color"])
            print("profile_background_image_url:" + dictData["profile_background_image_url"])
            print("profile_background_image_url_https:" + dictData["profile_background_image_url"])
            print("profile_background_image_url:" + dictData["profile_background_image_url"])
            print("profile_background_tile:" + dictData["profile_background_tile"])
            print("profile_link_color:" + dictData["profile_link_color"])
            print("profile_sidebar_border_color:" + dictData["profile_sidebar_border_color"])
            print("profile_sidebar_fill_color:" + dictData["profile_sidebar_fill_color"])
            print("profile_text_color:" + dictData["profile_text_color"])
            print("profile_use_background_image:" + dictData["profile_use_background_image"])
            print("profile_image_url:" + dictData["profile_image_url"])
            print("profile_image_url_https:" + dictData["profile_image_url_https"])
            print("profile_banner_url:" + dictData["profile_banner_url"])
            print("default_profile:" + dictData["default_profile"])
            print("default_profile_image:" + dictData["default_profile_image"])
            print("following:" + dictData["following"])
            print("follow_request_sent:" + dictData["follow_request_sent"])
            print("notifications:" + dictData["notifications"])
            print("coordinates:" + dictData["coordinates"])
            print("place_type:" + dictData["place_type"])
            print("place_full_name:" + dictData["full_name"])
            print("country_code:" + dictData["country_code"])
            print("country_code:" + dictData["country_code"])
            print("country_code:" + dictData["country_code"])
            print("country_code:" + dictData["country_code"])
            print("country_code:" + dictData["country_code"])
            print("country_code:" + dictData["country_code"])
            print("country_code:" + dictData["country_code"])
            """
            print("\n")
			#mapping with key-value pair method
            # grab the wanted data from the Tweet
            id = (dictData["id"])
            created_at = (dictData["created_at"])
            text = (dictData["text"])
            id_str = (dictData["id_str"])
            favorited = (dictData["favorited"])
            retweet_count = (dictData["retweet_count"])
            favorite_count = (dictData["favorite_count"])
            source = (dictData["source"])
            in_reply_to_status_id = dictData["in_reply_to_status_id"]
            in_reply_to_status_id_str = str(dictData["in_reply_to_status_id_str"])
            in_reply_to_user_id = dictData["in_reply_to_user_id"]
            in_reply_to_user_id_str = str(dictData["in_reply_to_user_id_str"])
            in_reply_to_screen_name = dictData["in_reply_to_screen_name"]
            # screen_name = datajson['user']['screen_name']

            created_at = str(dictData["user"]["created_at"])
            default_profile = str(dictData["user"]["default_profile"])
            default_profile_image = str(dictData["user"]["default_profile_image"])
            followers_count = str(dictData["user"]["followers_count"])
            follow_request_sent = str(dictData["user"]["follow_request_sent"])
            favourites_count = str(dictData["user"]["favourites_count"])
            geo_enabled = str(dictData["user"]["geo_enabled"])



            # user data
            u_id = str(dictData["user"]["id"])
            id_str = str(dictData["user"]["id_str"])
            lang = str(dictData["user"]["lang"])
            listed_count = str(dictData["user"]["listed_count"])
            location = str(dictData["user"]["location"])
            name = str(dictData["user"]["name"])
            profile_background_image_url = str(dictData["user"]["profile_background_image_url"])
            profile_background_image_url_https = str(dictData["user"]["profile_background_image_url_https"])
            profile_background_tile = str(dictData["user"]["profile_background_tile"])
            profile_image_url = str(dictData["user"]["profile_image_url"])
            profile_image_url_https = str(dictData["user"]["profile_image_url_https"])
            profile_link_color = str(dictData["user"]["profile_link_color"])
            profile_sidebar_border_color = str(dictData["user"]["profile_sidebar_border_color"])
            profile_sidebar_fill_color = str(dictData["user"]["profile_sidebar_fill_color"])
            profile_text_color = str(dictData["user"]["profile_text_color"])
            profile_use_background_image = str(dictData["user"]["profile_use_background_image"])
            protected = str(dictData["user"]["protected"])
            screen_name = str(dictData["user"]["screen_name"])
            url = str(dictData["user"]["url"])
            utc_offset = str(dictData["user"]["utc_offset"])
            verified = str(dictData["user"]["verified"])
            statuses_count = str(dictData["user"]["statuses_count"])
            time_zone = str(dictData["user"]["time_zone"])
            tweet_id = (dictData["id"])
            contributors_enabled = str(dictData["user"]["contributors_enabled"])
			#place data mapping
            place_type = str(dictData["place"]["place_type"])
            country_code = str(dictData["place"]["country_code"])
            full_name = str(dictData["place"]["full_name"])
            p_id = str(dictData["place"]["id"])
            p_name = str(dictData["place"]["name"])
            p_url = str(dictData["place"]["url"])

            # show_all_line_media=str(dictData["user"]["show_all_line_media"])
            is_translator = str(dictData["user"]["is_translator"])

            # print out a message to the screen that we have collected a tweet
            print("Tweet collected at " + str(created_at))
			
			
			
			#calling out all db connection functions (place_data,user_data,store_data) to store data in DB
            # insert the data into the MySQL database
            store_data(id, created_at, text, id_str, favorited, retweet_count, favorite_count, source
                       , in_reply_to_status_id, in_reply_to_status_id_str, in_reply_to_user_id, in_reply_to_user_id_str
                       , in_reply_to_screen_name)

            # insert user data into the MySQL database
            user_data(u_id, id_str, lang, listed_count, location, name, profile_background_image_url,
                      profile_background_image_url_https,
                      profile_background_tile,
                      profile_image_url,
                      profile_image_url_https,
                      profile_sidebar_border_color,
                      profile_sidebar_fill_color,
                      profile_text_color,
                      profile_use_background_image,
                      protected,
                      screen_name,
                      url,
                      utc_offset,
                      verified,
                      statuses_count, time_zone, tweet_id, contributors_enabled)

            # data about place
            place_data(place_type, country_code, full_name, p_id, p_name, p_url, tweet_id)

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


# Changing file name to save tweets in JSON format that searched by location
fileName = 'tweetsByLocations.json'

# Opening file to overwrite
saveFile = open(fileName, 'w')
# closing file
saveFile.close()

# Input geolocation from the user
# Get how many location that the user want
size = int(input("How many locations you would like to search from?: "))

if (size > 0):
    for i in range(int(size)):
        geoLocations = list()
        inDefault = int(input("Enter 0 for default or enter 1 for entering other geolocation: "))
        if (inDefault == 0):
            geoLocations = defaultLocation
        if (inDefault == 1):
            geoLocations = inputLocations()
		
        print("\nCollecting tweets that originated from the geographic region around " + str(geoLocations) + "\n")
        # Stream tweets that filter by the geolocation that the user put in
        tweepy.Stream(auth=api.auth, listener=MyStreamListener()).filter(locations=geoLocations)



