from urllib.request import urlopen
from pytube import YouTube
import imgurpython
import re
import praw
import random
import requests
import bs4
import moviepy


# link to the How it's made youtube video query
linkQuery = "https://www.youtube.com/results?search_query=how+its+made"

# pages is a list to hold all links so we don't recieve duplicates
pages = set()

# reddit credentials
redditUsername = "LewisTheRobot"
redditPassword = "lewismenelaws"


# function to grab the youtube video link
def findYoutubeVideoLink(youtubeLinkQuery):
    global pages
    print("Finding Youtube video links...")
    html = urlopen(linkQuery)
    bsObj = bs4.BeautifulSoup(html, 'html.parser')
    # for every 'a' tag that has the '/watch' link...
    for link in bsObj.findAll("a", href=re.compile("^(/watch)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # We have encounted a new page
                newPage = link.attrs['href']
                print("Found new video at: https://youtube.com" + newPage)
                pages.add(newPage)
                return "https://youtube.com" + str(newPage)


# function that grabs the youtube video that has been grabbed by findYoutubeVideoLink
def downloadYoutubeVideo(youtubeLink):
    yt = YouTube(youtubeLink)
    video = yt.get('mp4')
    print("Downloading video... this may take a little bit...")
    video.download('videos/')
    print("Video downloaded!")


# function that takes youtube video and turns it into a gif
def turnYoutubeVideoIntoGif(youtubeVideo):
    print("You still got to do this shit lmfao")
    clip = ()


# Find package that converts mp4's to gifs..


youtube_link = findYoutubeVideoLink(linkQuery)
downloadYoutubeVideo(youtube_link)


