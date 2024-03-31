import inspect
import string
import sys

from Adafruit_IO import Client, RequestError, Feed, Data

sys.path.append('..')
import secrets

def send(data):
    if data is None:
        return

    aio = Client(secrets.AIO_USER_NAME, secrets.AIO_KEY)

    feed_name = f'{data["mac"].replace(":","")}-{data["sensor"]}'.lower()

    try:
        feed = aio.feeds(feed_name)
        print('feed exists')
        print(feed)
    except RequestError:
        #  The feed doesn't exist.  Create it!
        print('feed doesn\'t exist')
        new_feed = Feed(name=feed_name)
        feed = aio.create_feed(new_feed)
        print(f'create feed {feed_name}')
    aio.send_data(feed.key, data["value"])
    print(f'sending {feed_name} {data["value"]}')

