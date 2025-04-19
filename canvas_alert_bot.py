import discord
import asyncio
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

alert_queue = asyncio.Queue()

@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    bot.loop.create_task(process_alerts())

async def process_alerts():
    while True:
        user_id, message = await alert_queue.get()
        try:
            user = await bot.fetch_user(int(user_id))
            await user.send(message)
            print(f"Message sent to {user_id}")
        except Exception as e:
            print(f"Failed to send message to user {user_id}: {e}")

async def send_alert_message(user_id, message):
    await alert_queue.put((user_id, message))

def runBot():
    bot.run(TOKEN)
