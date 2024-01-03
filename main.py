from yt_dlp import YoutubeDL
import discord
import os
from decouple import config
import re
import asyncio

intents = discord.Intents.all()
client = discord.Client(intents=intents)

TOKEN = config('TOKEN')

@client.event
async def on_ready():
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
                    'cookiefile': 'cookies.txt',
                    'geo_bypass': True,
                }
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([convert_message])
                for file in os.listdir("./"):
                    if file.endswith(".mp4"):
                        os.rename(file, "video.mp4")
                        await message.channel.send(file=discord.File("video.mp4"))
                        await asyncio.sleep(5)  # Await for 5 seconds
                        os.remove("video.mp4")  # Remove the video file
                        
        except Exception as e:
            await message.channel.send(e)
            return
        
client.run(TOKEN)