import asyncio
import json
import aiohttp
import discord
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("TOKEN")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

async def fetchApi(payload):
    print()
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, headers=headers, json={"inputs": payload}) as response:
            r = await response.json()
            return r['conversation']['generated_responses'][0]




intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event

async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'{client.user.id}')
    print(f'{client.user.name}')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    elif message.channel.name == "test-bot":
        try:
            await message.channel.typing()
            await asyncio.sleep(2)
            resp = await fetchApi(message.content)  
            await message.channel.send(resp)
        except:
            await message.channel.send("Sorry, I can't understand you")
       
        

asyncio.get_event_loop().run_until_complete(client.run(DISCORD_TOKEN))


