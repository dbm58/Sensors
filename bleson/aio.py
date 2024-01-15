from Adafruit_IO import Client, RequestError, Feed, Data

import secrets

class Aio:
    @classmethod
    def send(cls, mac, value, feed_name):
        if feed_name is None:
            return

        if value is None:
            return

        feed_mac = mac.replace(':', '').lower()
        feed_key = f'{feed_mac}-{feed_name}'

        print('sending', feed_key, value)

        aio = Client(secrets.AIO_USER_NAME, secrets.AIO_KEY)
        try:
            feed = aio.feeds(feed_key)
        except RequestError:
            print('creating feed', feed_key)
            new_feed = Feed(name=feed_key)
            feed = aio.create_feed(new_feed)
        aio.send_data(feed.key, value)
