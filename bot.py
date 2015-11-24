# Imports
from urllib.request import urlopen
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube
from decimal import Decimal
import imgurpython
import re
import praw
import random
import bs4
import subprocess
import os

directoryFlag = False

# link to the How it's made youtube video query
linkQuery = "https://www.youtube.com/results?search_query=how+its+made"

# pages is a list to hold all youtube links so we don't recieve any duplicates
pages = set()

# Easy naming scheme for the videos and gifs
videoName = 0
gifName = 0

# imgur credentials
imgurClientId = "b01297eb68376c7"
imgurClientSecret = "0f7006ff650c755924a1cf531036c4820cfd8c72"

# reddit credentials
redditUsername = "LewisTheRobot"
redditPassword = "lewismenelaws"


# function that will check to see if you have 'videos' and 'gifs'
def createFolders():
    global directoryFlag
    print("Creating directory for videos")
    os.makedirs("videos", exist_ok=True)
    print("Creating directory for gifs")
    os.makedirs("gifs", exist_ok=True)
    directoryFlag = True


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
    process = subprocess.Popen(['/usr/local/bin/ffmpeg', '-i', youtubeVideo], stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    # matches does a regex scan and finds duration of video that has been downloaded
    matches = re.search(r"Duration:\s(?P<hours>\d+?):(?P<minutes>\d+?):(?P<seconds>\d+\.\d+?),",
                        str(stdout)).groupdict()
    hours = int(matches['hours'])
    minutes = int(matches['minutes'])
    seconds = int(Decimal(matches['seconds']))
    print("Length of video is: " + str(minutes) + " minutes. As well as " + str(Decimal(seconds)) + " seconds.")
    return matches['minutes'], matches['seconds']


# function that takes youtube video and turns it into a gif
# Currently the gifs are set to be 3.5 seconds long.
def turnYoutubeVideoIntoGif(youtubeVideo, minutes, seconds):
    global gifName
    # randomize points of the video
    randomLengthMinutes = random.randint(0, int(minutes))
    randomLengthSeconds = random.randint(0, int(Decimal(seconds)))
    randomLengthSecondsEnd = int(randomLengthSeconds) + 3.5
    gifName += 1
    print("Converting video into gif...")
    clip = (VideoFileClip(youtubeVideo)
            .subclip((int(randomLengthMinutes), int(randomLengthSeconds)),
                     (int(randomLengthMinutes), int(randomLengthSecondsEnd))))
    clip.write_gif("gifs/how-its-made" + str(gifName) + ".gif", fps=15)
    print("Gif has been created!!!")
    return "gifs/how-its-made" + str(gifName) + ".gif"


# Takes gif and uploads to imgur and returns upload link in order to upload to reddit
def uploadGifToImgur(gif, clientId, clientSecret):
    # Uploading Gif to Imgur
    print("Uploading " + gif + " to imgur.")
    i = imgurpython.ImgurClient(clientId, clientSecret).upload_from_path(path=gif, config=None, anon=True)
    link = i.get('link')
    print("Gif can be found at: " + link)
    return link


def uploadGifToReddit(imgurLink, username, password):
    global gifName
    r = praw.Reddit(user_agent="How its made!!")
    r.login(redditUsername, redditPassword)
    subreddit = r.get_subreddit("LewisTestsBots")
    print("Uploading link to reddit")
    subreddit.submit(title="How it's made " + str(gifName), url=imgurLink)





# Main Loop
while True:
    if directoryFlag is False:
        createFolders()
    youtube_link = findYoutubeVideoLink(linkQuery)
    youtubeVideo = downloadYoutubeVideo(youtube_link)
    (minutes, seconds) = grabTimeOfDownloadedYoutubeVideo(youtubeVideo)
    urlPath = turnYoutubeVideoIntoGif(youtubeVideo, minutes, seconds)
    imgurLink = uploadGifToImgur("gifs/" + "how-its-made" + str(gifName) + ".gif", imgurClientId, imgurClientSecret)
    uploadGifToReddit(imgurLink, redditUsername, redditPassword)


    # todo - post imgur link to reddit
