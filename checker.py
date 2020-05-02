from bs4 import BeautifulSoup
import requests
import pyshorteners
import time
import tweepy
import datetime

# Setting Api keys

auth = tweepy.OAuthHandler("consumer_key",
                           "consumer_secret")
auth.set_access_token("Access_token",
                      "Access_token_secret")
api = tweepy.API(auth)

s = pyshorteners.Shortener(api_key='bit.ly API secret')
bfv_seen = set()

# Check twitter api authentication
try:
    api.verify_credentials()
    print("Twitter Authentication OK")
except:
    print("Error during authentication")


def start():
    # Battlefield V
    page = requests.get(
        'https://www.ea.com/games/battlefield/battlefield-5/news')
    soup = BeautifulSoup(page.text, 'html.parser')
    grid = soup.find("ea-grid")
    news = grid.find(slot="container")
    copy = news.find(slot="copy").text
    title = news.find("h3").text
    link = news.find("a")
    url = s.bitly.short("https://www.ea.com" + link.get('href'))
    now = datetime.datetime.now()
    print("Last time checked:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("Checking Battlefield updates...")
    with open('last_seen.txt') as f:
        if link.get('href') not in f.read():
            f = open("last_seen.txt", "w+")
            f.write(link.get('href'))
            bfv_seen.add(link.get('href'))
            print("Sending tweet...")
            api.update_status(f"{title} \n #BattlefieldV {url}")
            f.close()


while True:
    start()
    time.sleep(60)
