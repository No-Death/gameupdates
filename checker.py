from bs4 import BeautifulSoup
import requests
import pyshorteners
import time
import tweepy
import datetime
import os
import logging
from configparser import ConfigParser

config = ConfigParser()

config['API Tokens'] = {
    'Twitter_Consumer_Key': '',
    'Twitter_Consumer_Secret': '',
    'Twitter_Access_Token': '',
    'Twitter_Access_Token_Secret': '',
    'Bit.ly_Secret_Token': ''
}
config['Settings'] = {
    'Search_Delay': ''
}

config.read('config.ini')

c_token = config.get('API Tokens', 'Twitter_Consumer_Key')
c_secret = config.get('API Tokens', 'Twitter_Consumer_Secret')
a_token = config.get('API Tokens', 'Twitter_Access_Token')
a_secret = config.get('API Tokens', 'Twitter_Access_Token_Secret')
b_secret = config.get('API Tokens', 'Bit.ly_Secret_Token')
sd = config.getint('Settings', 'Search_Delay')

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter(
    '%(asctime)s : %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Setting Api keys
auth = tweepy.OAuthHandler(c_token, c_secret)
auth.set_access_token(a_token, a_secret)
api = tweepy.API(auth)

s = pyshorteners.Shortener(api_key=b_secret)

# Check twitter api authentication
try:
    api.verify_credentials()
    print("Twitter Authentication OK")
except:
    print("Error during authentication")


def start():

    # Battlefield V
    try:
        page = requests.get(
            'https://www.ea.com/games/battlefield/battlefield-5/news')
        soup = BeautifulSoup(page.text, 'html.parser')
        grid = soup.find("ea-grid")
        news = grid.find(slot="container")
        copy = news.find(slot="copy").text
        title = news.find("h3").text
        link = news.find("a")
        url = s.bitly.short("https://www.ea.com" + link.get('href'))
    except AttributeError as e:
        print("Battlefield Check Error:", e)
        logger.exception("Battlefield Check Error")
        pass
    except pyshorteners.exceptions as e:
        print(e)
        logger.exception("Url Shortener Error")
        pass
    else:
        print("Checking Battlefield updates...")
        with open('seen/bfv_seen.txt') as f:
            if link.get('href') not in f.read():
                try:
                    f = open("seen/bfv_seen.txt", "w+")
                    f.write(link.get('href'))
                    print("Sending tweet...")
                    api.update_status(f"{title} \n #BattlefieldV {url}")
                    f.close()
                    pass
                except tweepy.TweepError as e:
                    print(e)
                    logger.exception("Twitter API Error")
                    time.sleep(60)
                    pass

    # Risk of Rain 2
    try:
        page = requests.get(
            'https://store.steampowered.com/news/?appids=632360')
        soup = BeautifulSoup(page.text, 'html.parser')
        news = soup.find(id="news")
        title = news.find(class_="posttitle").text
        link = news.find("a")
        url = s.bitly.short(link.get("href"))
    except AttributeError as e:
        print("Risk of Rain 2 Check Error:", e)
        logger.exception("Risk of Rain 2 Check Error")
        pass
    except pyshorteners.exceptions as e:
        print(e)
        logger.exception("Url Shortener Error")
        pass
    else:
        print("Checking Risk of Rain 2 updates...")
        with open('seen/ror2_seen.txt') as f:
            if link.get('href') not in f.read():
                try:
                    f = open("seen/ror2_seen.txt", "w+")
                    f.write(link.get('href'))
                    print("Sending tweet...")
                    api.update_status(f"{title} \n #RoR2 {url}")
                    f.close()
                    pass
                except tweepy.TweepError as e:
                    print(e)
                    logger.exception("Twitter API Error")
                    time.sleep(60)
                    pass


while True:
    try:
        requests.get("http://google.com")
        start()
        time.sleep(sd)
        os.system('cls')
        now = datetime.datetime.now()
        print("Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
    except requests.exceptions.RequestException:
        print("Connection error, retrying in 5 minutes.")
        logger.exception("Network Error")
        time.sleep(300)
