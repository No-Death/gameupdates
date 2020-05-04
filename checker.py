from bs4 import BeautifulSoup
import requests
import pyshorteners
import time
import tweepy
import datetime
import os
import sys
import logging
from configparser import ConfigParser

config = ConfigParser()


def write_cfg():
    config.write(open('config.ini', 'w'))


if not os.path.exists('config.ini'):
    config['API Tokens'] = {
        'Twitter_Consumer_Key': '',
        'Twitter_Consumer_Secret': '',
        'Twitter_Access_Token': '',
        'Twitter_Access_Token_Secret': '',
        'Bit.ly_Secret_Token': ''
    }
    config['Settings'] = {
        'Search_Delay': '60'
    }
    write_cfg()
else:
    config.read('config.ini')


c_token = config.get('API Tokens', 'Twitter_Consumer_Key')
c_secret = config.get('API Tokens', 'Twitter_Consumer_Secret')
a_token = config.get('API Tokens', 'Twitter_Access_Token')
a_secret = config.get('API Tokens', 'Twitter_Access_Token_Secret')
b_secret = config.get('API Tokens', 'Bit.ly_Secret_Token')
sd = config.getint('Settings', 'Search_Delay')

# Setting Up Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('logfile.log')
formatter = logging.Formatter(
    '%(asctime)s : %(levelname)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Setting API Keys
auth = tweepy.OAuthHandler(c_token, c_secret)
auth.set_access_token(a_token, a_secret)
api = tweepy.API(auth)
s = pyshorteners.Shortener(api_key=b_secret)

# Check Twitter API Authentication
try:
    api.verify_credentials()
    print("Twitter Authentication OK")
except:
    print("Error During Authentication")
    logger.exception("Error During Authentication")


def sleep():
    for remaining in range(sd, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Sleeping for {:2d} seconds.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)


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
        print("Battlefield V Check Error:", e)
        logger.exception("Battlefield V Check Error")
        pass
    except (pyshorteners.exceptions.BadAPIResponseException, pyshorteners.exceptions.ShorteningErrorException, pyshorteners.exceptions.BadURLException, pyshorteners.exceptions.ExpandingErrorException) as e:
        print("Url Shortener Error")
        logger.exception("Url Shortener Error")
        pass
    except requests.exceptions.RequestException:
        print("Connection Error, Retrying In 5 Minutes.")
        logger.exception("Network Error")
        time.sleep(300)
        pass
    else:
        print("Checking Battlefield V updates...")
        with open('seen/bfv_seen.txt') as f:
            if link.get('href') not in f.read():
                try:
                    f = open("seen/bfv_seen.txt", "w+")
                    f.write(link.get('href'))
                    print(title, url)
                    print("Sending tweet...")
                    api.update_status(f"{title} \n #BattlefieldV {url}")
                    f.close()
                    logger.info(f'Sent a Battlefield V Tweet\n{title} {url}')
                    pass
                except tweepy.TweepError as e:
                    print(e)
                    logger.exception("Twitter API Error")
                    time.sleep(60)
                    pass
                except requests.exceptions.RequestException:
                    print("Connection Error, Retrying In 5 Minutes.")
                    logger.exception("Network Error")
                    time.sleep(300)
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
    except (pyshorteners.exceptions.BadAPIResponseException, pyshorteners.exceptions.ShorteningErrorException, pyshorteners.exceptions.BadURLException, pyshorteners.exceptions.ExpandingErrorException) as e:
        print("Url Shortener Error")
        logger.exception("Url Shortener Error")
        pass
    except requests.exceptions.RequestException:
        print("Connection Error, Retrying In 5 Minutes.")
        logger.exception("Network Error")
        time.sleep(300)
        pass
    else:
        print("Checking Risk of Rain 2 updates...")
        with open('seen/ror2_seen.txt') as f:
            if link.get('href') not in f.read():
                try:
                    f = open("seen/ror2_seen.txt", "w+")
                    f.write(link.get('href'))
                    print(title, url)
                    print("Sending tweet...")
                    api.update_status(f"{title} \n #RoR2 {url}")
                    f.close()
                    logger.info(f'Sent a Risk of Rain 2 Tweet\n{title} {url}')
                    pass
                except tweepy.TweepError as e:
                    print(e)
                    logger.exception("Twitter API Error")
                    time.sleep(60)
                    pass
                except requests.exceptions.RequestException:
                    print("Connection Error, Retrying In 5 Minutes.")
                    logger.exception("Network Error")
                    time.sleep(300)
                    pass

    # Post Scriptum
    try:
        page = requests.get(
            'https://store.steampowered.com/news/?appids=736220')
        soup = BeautifulSoup(page.text, 'html.parser')
        news = soup.find(id="news")
        title = news.find(class_="posttitle").text
        link = news.find("a")
        url = s.bitly.short(link.get("href"))
    except AttributeError as e:
        print("Post Scriptum Check Error:", e)
        logger.exception("Post Scriptum Check Error")
        pass
    except (pyshorteners.exceptions.BadAPIResponseException, pyshorteners.exceptions.ShorteningErrorException, pyshorteners.exceptions.BadURLException, pyshorteners.exceptions.ExpandingErrorException) as e:
        print("Url Shortener Error")
        logger.exception("Url Shortener Error")
        pass
    except requests.exceptions.RequestException:
        print("Connection Error, Retrying In 5 Minutes.")
        logger.exception("Network Error")
        time.sleep(300)
        pass
    else:
        print("Checking Post Scriptum updates...")
        with open('seen/ps_seen.txt') as f:
            if link.get('href') not in f.read():
                try:
                    f = open("seen/ps_seen.txt", "w+")
                    f.write(link.get('href'))
                    print(title, url)
                    print("Sending tweet...")
                    api.update_status(f"{title} \n #PostScriptum {url}")
                    f.close()
                    logger.info(f'Sent a Post Scriptum Tweet\n{title} {url}')
                    pass
                except tweepy.TweepError as e:
                    print(e)
                    logger.exception("Twitter API Error")
                    time.sleep(60)
                    pass
                except requests.exceptions.RequestException:
                    print("Connection Error, Retrying In 5 Minutes.")
                    logger.exception("Network Error")
                    time.sleep(300)
                    pass

    # Factorio
    try:
        page = requests.get(
            'https://store.steampowered.com/news/?appids=427520')
        soup = BeautifulSoup(page.text, 'html.parser')
        news = soup.find(id="news")
        title = news.find(class_="posttitle").text
        link = news.find("a")
        url = s.bitly.short(link.get("href"))
    except AttributeError as e:
        print("Factorio Check Error:", e)
        logger.exception("Factorio Check Error")
        pass
    except (pyshorteners.exceptions.BadAPIResponseException, pyshorteners.exceptions.ShorteningErrorException, pyshorteners.exceptions.BadURLException, pyshorteners.exceptions.ExpandingErrorException) as e:
        print("Url Shortener Error")
        logger.exception("Url Shortener Error")
        pass
    except requests.exceptions.RequestException:
        print("Connection Error, Retrying In 5 Minutes.")
        logger.exception("Network Error")
        time.sleep(300)
        pass
    else:
        print("Checking Factorio updates...")
        with open('seen/Factorio_seen.txt') as f:
            if link.get('href') not in f.read():
                try:
                    f = open("seen/factorio_seen.txt", "w+")
                    f.write(link.get('href'))
                    print(title, url)
                    print("Sending tweet...")
                    api.update_status(f"{title} \n #Factorio {url}")
                    f.close()
                    logger.info(f'Sent a Factorio Tweet\n{title} {url}')
                    pass
                except tweepy.TweepError as e:
                    print(e)
                    logger.exception("Twitter API Error")
                    time.sleep(60)
                    pass
                except requests.exceptions.RequestException:
                    print("Connection Error, Retrying In 5 Minutes.")
                    logger.exception("Network Error")
                    time.sleep(300)
                    pass


while True:
    try:
        requests.get("http://google.com")
        start()
        sleep()
        os.system('cls')
        now = datetime.datetime.now()
        print("Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
    except requests.exceptions.RequestException:
        print("Connection Error, Retrying In 5 Minutes.")
        logger.exception("Network Error")
        time.sleep(300)
