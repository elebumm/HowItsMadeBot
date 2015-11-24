# Imports
from urllib.request import urlopen
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
import requests
import imgurpython
import re
import praw
import random
import bs4
import subprocess
from decimal import Decimal

# link to the How it's made youtube video query
linkQuery = "https://www.youtube.com/results?search_query=how+its+made"

# pages is a list to hold all links so we don't recieve duplicates
pages = set()

# Fairly standard naming scheme...
videoName = 0
gifName = 0

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
    global videoName
    videoName += 1
    yt = YouTube(youtubeLink)
    yt.set_filename(videoName)
    # Sadly low quality however it's usually the only one available (Seriously science channel...)
    video = yt.get('mp4', '360p')
    print("Downloading video... this may take a little bit...")
    video.download('videos/')
    print("Video downloaded at videos/" + str(videoName) + '.mp4!')
    return 'videos/' + str(videoName) + '.mp4'


# function that grabs time of the video downloaded in order to grab a random time later on
# Uses ffmpeg to grab time of the youtube video that has been downloaded
def grabTimeOfDownloadedYoutubeVideo(youtubeVideo):
    process = subprocess.Popen(['/usr/local/bin/ffmpeg', '-i', youtubeVideo], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    # matches does a regex scan and finds duration of video that has been downloaded
    matches = re.search(r"Duration:\s(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),", str(stdout)).groupdict()
    hours = int(matches['hours'])
    minutes = int(matches['minutes'])
    seconds = int(Decimal(matches['seconds']))
    print("Length of video is: " + str(minutes) + " minutes. As well as " + str(Decimal(seconds)) + " seconds.")
    return matches['minutes'], matches['seconds']


# function that takes youtube video and turns it into a gif
def turnYoutubeVideoIntoGif(youtubeVideo, minutes, seconds):
    global gifName
    # randomize points of the video
    randomLengthMinutes = random.randint(0, int(minutes))
    randomLengthSeconds = random.randint(0, int(Decimal(seconds)))
    randomLengthSecondsEnd = int(randomLengthSeconds) + 4
    gifName += 1
    print("Converting video into gif...")
    clip = (VideoFileClip(youtubeVideo)
            .subclip((int(randomLengthMinutes), int(randomLengthSeconds)), (int(randomLengthMinutes), int(randomLengthSecondsEnd))))
    clip.write_gif("gifs/how-its-made" + str(gifName) + ".gif")
    print("Gif has been created!!!")


# Takes gif and uploads to imgur and returns upload link in order to upload to reddit
def uploadGifToImgur(gif):
    print("todo")


while True:
    youtube_link = findYoutubeVideoLink(linkQuery)
    youtubeVideo = downloadYoutubeVideo(youtube_link)
    (minutes, seconds) = grabTimeOfDownloadedYoutubeVideo(youtubeVideo)
    turnYoutubeVideoIntoGif(youtubeVideo, minutes, seconds)

