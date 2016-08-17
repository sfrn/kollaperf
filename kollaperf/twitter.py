import logging
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from kollaperf.label import generate_and_print
from kollaperf.config import settings

twitter_settings = settings['twitter']
log = logging.getLogger(__name__)

def is_appropriate(text):
    for term in twitter_settings['track']:
        if all(word in text for word in term.split(' ')):
            return True
    return False

class PrintingListener(StreamListener):
    def __init__(self, machine):
        self.machine = machine

    def on_data(self, data):
        try:
            info = json.loads(data)
            text = info['text']
            if is_appropriate(text):
                log.info('Collected tweet {} ({})...'.format(info['id_str'], info['text']))
                self.machine.collect_tweet(info['text'])
        except Exception as e:
            log.exception(e)

    def on_error(self, status):
        log.error(status)

def start_async(machine):
    l = PrintingListener(machine)
    auth = OAuthHandler(twitter_settings['consumer_key'], twitter_settings['consumer_secret'])
    auth.set_access_token(twitter_settings['access_token'], twitter_settings['access_token_secret'])

    stream = Stream(auth, l)
    print(twitter_settings['track'])
    stream.filter(track=twitter_settings['track'], async=True)

