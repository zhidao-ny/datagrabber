
# coding: utf-8

# In[1]:


from tweepy import StreamListener
import json
import time
import sys

class SListener(StreamListener):
    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or API()
        self.counter = 0
        #self.fprefix = fprefix
        self.output  = open('twitter_stream.json', 'w')
        #self.output  = open('%s_%s.json' % (self.fprefix, time.strftime('%Y%m%d-%H%M%S')), 'w')
        

    def on_data(self, data):
        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print("WARNING: %s" % warning['message'])
            return


    def on_status(self, status):
        self.counter += 1
        
        if self.counter <=1000:
            print(status)
            self.output.write(status)
            return True
        else:
            self.output.close()
            return False


    def on_delete(self, status_id, user_id):
        print("Delete notice")
        return


    def on_limit(self, track):
        print("WARNING: Limitation notice received, tweets missed: %d" % track)
        return


    def on_error(self, status_code):
        print('Encountered error with status code:', status_code)
        return 


    def on_timeout(self):
        print("Timeout, sleeping for 60 seconds...")
        time.sleep(60)
        return
    


from tweepy import OAuthHandler
from tweepy import API

# Consumer key authentication
auth = OAuthHandler('myFxjsjnTxoDmQEjgOosdK94d', 'vnkWFpftaTg5Q4OYoAuO5pECL3uFZuZZDHFNBxwQdb4UcvkXCY')

# Access key authentication
auth.set_access_token('815963681854996480-GyUT29WFx3N1PeNpCt9kxzBU8z0lY6B', 
                      'DbXYDeHxrigz42a8lwBIHOxFj13A6i9NgSSAoQS1Oe2oN')

# Set up the API with the authentication handler
api = API(auth)

from tweepy import Stream

# Set up words to track
keywords_to_track = ['Ajax','API','ASP.NET','Agile','Algorithms','AWS','MongoDB','Python','C++','Java','Javascript',
                    'Android','Angular','Kafka','Spark','Zookeeper','Hadoop','iOS','Linux','PostgreSQL','NoSQL',
                    'MySQL','SQLite','GCP','React','node.js','Tensorflow','Kotlin','Groovy','HTML','HTML5','CSS',
                    'PHP','jQuery','Cloud Computing','Deep learning','swift','Golang','C#']

# Instantiate the SListener object 
listen = SListener(api)

# Instantiate the Stream object
stream = Stream(auth, listen)

# Begin collecting data
stream.filter(track = keywords_to_track, languages=["en"])

