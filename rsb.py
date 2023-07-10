import praw
import asyncio
from pyrogram import Client

telegram_chat_id = ['']

# Reddit API credentials
reddit_client_id = ''
reddit_client_secret = ''
reddit_user_agent = ''

reddit = praw.Reddit(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

app = Client("rbot", bot_token="", api_id=6, api_hash="eb06d4abfb49dc3eeb1aeb98ae0f581e")

# Set to store processed post IDs
processed_post_ids = set()

# Function to send a Reddit post to Telegram
async def send_post_to_telegram(post):
    message = f"Title: {post.title}\n\n{post.url}"
    await app.send_message(chat_id=telegram_chat_id, text=message)

# Function to monitor and send new Reddit posts to Telegram
async def monitor_reddit_channel():
    subreddit = reddit.subreddit('memes')
    while True:
        async for post in subreddit.stream.submissions():
            if post.id not in processed_post_ids:
                await send_post_to_telegram(post)
                processed_post_ids.add(post.id)
        await asyncio.sleep(10)

app.start()
idle()
