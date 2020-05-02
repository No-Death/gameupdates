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
    print("Time:", now.strftime("%Y-%m-%d %H:%M:%S"))
    print("Checking Battlefield updates...")
    with open('seen/bfv_seen.txt') as f:
        if link.get('href') not in f.read():
            try:
                f = open("seen/bfv_seen.txt", "w+")
                f.write(link.get('href'))
                print("Sending tweet...")
                # api.update_status(f"{title} \n #BattlefieldV {url}")
                f.close()
                pass
            except tweepy.TweepError as e:
                print(e)
                time.sleep(60)
                pass

    # Risk of Rain 2
    page = requests.get(
        'https://store.steampowered.com/news/?appids=632360')
    soup = BeautifulSoup(page.text, 'html.parser')
    news = soup.find(id="news")
    title = news.find(class_="posttitle").text
    link = news.find("a")
    url = s.bitly.short(link.get("href"))
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
                time.sleep(60)
                pass


while True:
    try:
        requests.get("http://google.com")
        start()
        time.sleep(60)
    except requests.exceptions.RequestException:
        print("Connection error, retrying in 5 minutes.")
        time.sleep(300)
