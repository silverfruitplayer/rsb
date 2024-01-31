import praw
from prawcore.exceptions import NotFound
import asyncio
from pyrogram import Client, filters, idle
from pyrogram.types import Message
import logging
import requests
import os
from random import choice
import time
from pyrogram.errors.exceptions.flood_420 import FloodWait 

# Reddit API credentials
reddit_client_id = 'PwIeyGTeEHK6DQNAylKG2Q'
reddit_client_secret = 'Lb511Fz1gVqcU2VTTHtWyUu2BanUtg'
reddit_user_agent = 'rstream'
#reddit_subreddit = 'Animemes'

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent,
    username="stebin58",
    redirect_uri="http://localhost:8080"
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

app = Client("rstreambot", bot_token="6203076674:AAGec-30uhR8D2f7nFaz0XSUpGySARJ6T1U", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

os.makedirs("images/", exist_ok=True)
print("Successfully Set Directory As :images:")

@app.on_message(filters.command("send"))
async def send_posts_to_telegram(_, message):
    x = await message.reply("Checking...")   
    
    global stop_sending
    stop_sending = False
    
    try:
        # Extract subreddit name from user's message
        command, subreddit_name = message.text.split(maxsplit=1)
        
        # Check if subreddit_name is None or empty
        if not subreddit_name:
            return await x.edit("Subreddit name is missing in the command.\nUsage: /send <subreddit channel name>")
        
        # Retrieve the subreddit
        subreddit = reddit.subreddit(subreddit_name)
        
        for post in subreddit.stream.submissions():
            try:
                if post.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
                    # Download and send images
                    await send_image(post, message)
                elif post.is_video:
                    # Download and send videos
                    await send_video(post, message)

                if stop_sending:
                    break
            except Exception as e:
                print(f"Error processing post: {e}")

        await message.reply(f"All posts from /r/{subreddit_name} sent as images and videos.")
    except ValueError as e:
        return await message.reply(f"Subreddit name is missing in the command.\nUsage: /send <subreddit channel name>")
    except NotFound as e:
        return await message.reply(f"Subreddit not found. Please provide a valid subreddit.")
    except Exception as e:
        return await message.reply(f"An error occurred: {e}")

    await x.delete()



async def send_image(post, message):
    response = requests.get(post.url)
    if response.status_code == 200:
        file_path = f"images/{post.id}.jpg"
        with open(file_path, "wb") as f:
            f.write(response.content)

        try:
            await asyncio.sleep(10)
            await app.send_photo(chat_id=message.chat.id, photo=file_path, caption=post.title)
            os.remove(file_path)
        except FloodWait as e:
            wait_time = e.x
            await message.reply(f"Received FloodWait error. Waiting for {wait_time} seconds...")
            time.sleep(wait_time)


async def send_video(post, message):
    video_url = post.media["reddit_video"]["fallback_url"]
    response = requests.get(video_url)
    if response.status_code == 200:
        file_path = f"videos/{post.id}.mp4"
        with open(file_path, "wb") as f:
            f.write(response.content)

        try:
            await asyncio.sleep(10)
            await app.send_video(chat_id=message.chat.id, video=file_path, caption=post.title)
            os.remove(file_path)
        except FloodWait as e:
            wait_time = e.x
            await message.reply(f"Received FloodWait error. Waiting for {wait_time} seconds...")
            time.sleep(wait_time)


@app.on_message(filters.command("stop"))
async def stop_sending_images(_, message):
    global stop_sending
    stop_sending = True
    y = await message.reply("Stop signal received, cooldown!")
    await y.delete()


app.start()
idle()
