import praw
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
reddit_subreddit = 'PornhubComments'

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

app = Client("rbot", bot_token="6203076674:AAE9wnjKJHYovzXby86MqOMSf-LQ9QQx7Ok", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

os.makedirs("images/", exist_ok=True)




#telegram_chat_id = ['-1001894132283']
@app.on_message(filters.command("send"))
async def send_posts_to_telegram(_, message):
    x = await message.reply("Starting...")   
    
    global stop_sending
    stop_sending = False
    
    # Retrieve posts from Reddit
    subreddit = reddit.subreddit(reddit_subreddit)
    posts = subreddit.new(limit=20000000000000000000000000000000000000000000000000)  # Adjust the limit as needed
    
    for post in posts:
        if post.url.endswith((".jpg", ".jpeg", ".png", ".gif")):
            # Download the image
            response = requests.get(post.url)
            if response.status_code == 200:
                file_path = f"images/{post.id}.jpg"  # Save the image with the post ID as the filename
                with open(file_path, "wb") as f:
                    f.write(response.content)
                    
                # Send the image to Telegram channel
                try:
                    #await x.edit("Waiting for 10 seconds...")
                    await asyncio.sleep(10)
                    await app.send_photo(chat_id=message.chat.id, photo=file_path, caption=post.title)
                    os.remove(file_path)
                except FloodWait as e:
                    wait_time = e.x
                    await message.reply(f"Received FloodWait error. Waiting for {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                                    
        if stop_sending:
            break        

    await message.reply("All posts sent as images.")
    await x.delete()

@app.on_message(filters.command("stop"))
async def stop_sending_images(_, message):
    global stop_sending
    stop_sending = True
    y = await message.reply("Stopped. Bye!")
    await y.delete()


app.start()
idle()
