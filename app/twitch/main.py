import discord
from discord.ext import commands
import system.lib as lib
import requests


global client
client=None

all_cible=[["randomwatchertv",False],["sardoche",False]]


def __init__(bot_client:commands.Bot):
    global client
    client=bot_client
    
async def scan(cible):
    client_id = '102r1dl5s1bmukgpoxxuhjuqlknr7g'
    client_secret = '8ulexf3xkapq0kf5s42jf7t0ijj8sj'
    streamer_name = all_cible[cible][0]

    body = {
        'client_id': client_id,
        'client_secret': client_secret,
        "grant_type": 'client_credentials'
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)

    #data output
    keys = r.json()

    headers = {
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + keys['access_token']
    }

    stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)

    stream_data = stream.json()

    if len(stream_data['data']) == 1:
        if not all_cible[cible][1]:
            await client.get_channel(1002004810985381991).send(f"{streamer_name} is in live: {stream_data['data'][0]['title']} playing {stream_data['data'][0]['game_name']}\nhttps://www.twitch.tv/{streamer_name}")
            all_cible[cible][1]=True
        else:
            if all_cible[cible][1]:
                all_cible[cible][1]=False

async def scan_all():
    for cible in range(len(all_cible)):
        await scan(cible)


command=[]
task=[lib.Task(scan_all,seconds=60)]