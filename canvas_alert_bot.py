import discord
# print(discord.__version__)    
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.default()
intents.message_content = True 

load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

async def send_alert_message(user_id: int, message: str): 
    try:
        user = await bot.fetch_user(user_id)
        await user.send(message)
    except Exception as e:
        print(f"Failed to send message to user {user_id}: {e}")

def runBot():
    bot.run(TOKEN)

if __name__ == "__main__":
    if not TOKEN:
        print("Error: DISCORD_BOT_TOKEN environment variable not set.")
        exit(1)
    bot.run(TOKEN)


