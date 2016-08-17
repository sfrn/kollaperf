import logging
from collections import deque
from queue import Queue, Empty

from kollaperf.config import settings
from kollaperf.label import generate_and_print
from kollaperf.twitter import start_async

log = logging.getLogger(__name__)

def is_primary(text):
    text = text.lower()
    for term in settings['twitter']['primary_track']:
        if term in text:
            return True
    return False

class Machine:
    def __init__(self):
        self.primary_queue = Queue()
        self.secondary_queue = deque(maxlen=settings['twitter']['secondary_queue_length'])

        start_async(self)

    def collect_tweet(self, text):
        if is_primary(text):
            log.info('Putting tweet into primary queue...')
            self.primary_queue.put_nowait(text)
        else:
            self.secondary_queue.append(text)
            log.info('Putting tweet into secondary queue (new length: {})'.format(len(self.secondary_queue)))

    def run_forever(self):
        while True:
            try:
                primary_text = self.primary_queue.get(True, settings['twitter']['primary_timeout'])
                self.print_tweet(primary_text)
            except Empty:
                log.info('Timeout reached! Query secondary queue...')
                self.print_secondary()

    def print_secondary(self):
        if self.secondary_queue:
            text = self.secondary_queue.popleft()
            self.print_tweet(text)
        else:
            log.warning('Secondary queue is empty.')

    def print_tweet(self, text):
        try:
            generate_and_print(text)
        except Exception as exc:
            log.exception(exc)
