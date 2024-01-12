from yt_dlp import YoutubeDL
import discord
import os
from decouple import config
import re
import asyncio
import requests

intents = discord.Intents.all()
client = discord.Client(intents=intents)

TOKEN = config('TOKEN')
REPO_URL = config('REPO_URL')

# Updated path to include /app/data
data_directory = "/app/data"
if not os.path.exists(data_directory):
    os.makedirs(data_directory)
os.chdir(data_directory)

CURRENT_VERSION = "v0.0.1-beta"

def set_version():
    version_path = os.path.join(data_directory, "version.txt")
    with open(version_path, "w") as file:
        file.write(CURRENT_VERSION)

def get_version():
    version_path = os.path.join(data_directory, "version.txt")
    if not os.path.exists(version_path):
        with open(version_path, "w") as file:
            file.write(CURRENT_VERSION)
    with open(version_path, "r") as file:
        version = file.read()
    print("Current version: " + version)
    return version

def retrieve_latest_version():
    try:
        version = requests.get(REPO_URL + "/releases/latest").url.split("/")[-1]
        print("Latest version: " + version)
    except Exception as e:
        print("Error retrieving latest version: " + str(e))
        return None
    return version

def check_for_updates():
    if get_version() == retrieve_latest_version():
        print("Up to date!")
    else:
        print("Update available!")

@client.event
async def on_ready():
    check_for_updates()
    print("Bot is ready and running!")

@client.event
async def on_message(message):
    link = "https://www.instagram.com/reel/"
    if link in message.content:
        user_message = str(message.content)
        try:
            convert_message = (re.search("(?P<url>https?://.*?/reel/[^/\s]+)", user_message).group("url"))
        except AttributeError:
            # no match, ignore message
            return
        try:
            async with message.channel.typing():
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'outtmpl': '%(title)s.%(ext)s',
                    'merge_output_format': 'mp4',
                    'quiet': True,
                    'no_warnings': True,
                    'ignoreerrors': True,
                    'cookiefile': os.path.join(data_directory, 'cookies.txt'),
                    'geo_bypass': True,
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([convert_message])
                for file in os.listdir(data_directory):
                    if file.endswith(".mp4"):
                        video_path = os.path.join(data_directory, file)
                        os.rename(video_path, os.path.join(data_directory, "video.mp4"))
                        await message.channel.send(file=discord.File(os.path.join(data_directory, "video.mp4")))
                        await asyncio.sleep(5)  # Await for 5 seconds
                        os.remove(os.path.join(data_directory, "video.mp4"))  # Remove the video file
                        
        except Exception as e:
            await message.channel.send(str(e))
            return
        
try:
    client.run(TOKEN)
except Exception as e:
    print(str(e))
