import os
import random
import random

import requests
import twitter
from dotenv import load_dotenv

import requests
import time

load_dotenv()

# Consumer keys and access tokens, used for OAuth
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
bearer_token = os.getenv('bearer_token')

api = twitter.Api(consumer_key=consumer_key,
                  consumer_secret=consumer_secret,
                  access_token_key=access_token,
                  access_token_secret=access_token_secret,
                  tweet_mode='extended')


query = """query MyQuery {
  token(
    where: {creators: {creator_address: {_eq: "tz1gJde57Meuqb2xMYbapTPzgTZkiCmPAMZA"}}, fa_contract: {_in: [KT1U6EHmNxJTkvaWJ4ThczG4FSDaHC21ssvi, KT1KEa8z6vWXDJrVqtMrAeDVzsvxat3kHaCE]}, name: {}}
    order_by: {display_uri: asc}
    offset: xxOFFSETxx
    limit: 1
  ) {
    display_uri
    name
    fa_contract
    token_id
  }
}"""   


num_tokens = 1300
def get_token():
    url = 'https://data.objkt.com/v3/graphql'

    while(True):
        try:
            r = requests.post(url, json={'query': query.replace('xxOFFSETxx', str(random.randint(0, num_tokens)))})
            token = r.json()['data']['token'][0]
            if not '0x' in token['name']: continue
        except Exception as e:
            print(e)
            continue
        break
    return token

def resolve_ipfs(url):
    return url.replace('ipfs://', 'https://ipfs.io/ipfs/')

def resolve_ipfs_to_objkt_url(url):
    hash = url.replace('ipfs://', '')
    return  f'https://assets.objkt.media/file/assets-003/{hash}/display'


def resolve_ipfs_to_fxhash_image_url(url):
    hash = url.replace('ipfs://', '')
    return  f'https://media.fxhash.xyz/w_700/{hash}'

def get_tweet_message(message):
    return message + '\n\n#generativeart'


def tweet():
    token = get_token()
    print(token)
    text = get_tweet_message(token['name'])
    media_url = resolve_ipfs_to_fxhash_image_url(token['display_uri'])
    api.PostUpdate(text, media=media_url)


def sleep():
    data = requests.get(f'https://space.pifragile.com/pifragile/get-config').json()
    min_hrs = data['twitter_interval_min_hours']
    max_hrs = data['twitter_interval_max_hours']
    time.sleep(random.randint(int(min_hrs * 3600), int(max_hrs * 3600)))

while True:
    tweet()
    sleep()