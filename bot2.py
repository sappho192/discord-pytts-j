# Japanese TTS bot
# You should install discord and pynacl package with pip

import discord
from discord.ext.commands import Bot
from urllib import request, parse
from time import sleep
import json
from datetime import datetime
import os

intents = discord.Intents.default()
bot = Bot(command_prefix='!', intents=intents)
global settings
with open('settings.json', 'r') as file:
    settings = json.load(file)
print(json.dumps(settings))

class TTSSession:
    def __init__(self, userid):
        self.userid = userid
        date = datetime.now()
        timestamp = date.strftime("%Y-%b-%d-%H-%M-%S-%f")
        self.guid = f'{userid}_{timestamp}'
        print(f'uid created: {self.guid}')
        self.voice_channel = None
        self.isTTSEnabled = False

global ttsSessions
ttsSessions = dict()

def find_sessionKey(ctx):
        sessionKey = None
        for key in ttsSessions:
            userid = ttsSessions[key].userid
            if (userid == ctx.author.id):
                sessionKey = key
        return sessionKey

@bot.event
async def on_ready():
    print(f'logged in to {bot.user}')

@bot.command()
async def say(ctx, arg):
    encoded = parse.quote(str(arg))
    endpoint = settings['tts_api_endpoint']
    url = f'{endpoint}{encoded}'
    sessionKey = find_sessionKey(ctx)
    if (sessionKey != None):
        session : TTSSession = ttsSessions[sessionKey]
        filepath = f'{session.guid}.wav'
        request.urlretrieve(url, filepath)
        session.voice_channel.play(discord.FFmpegPCMAudio(source=filepath))
    else:
        await ctx.send(f'Can\'t find session for {ctx.author.name}')

@bot.command()
async def tts2(ctx):
    session : TTSSession = find_sessionKey(ctx)
    if(session == None):
        # Join voice chat
        try:
            print('Joining voice chat')
            voice_channel = ctx.author.voice.channel
            if voice_channel != None:
                # Create TTSSession
                session = TTSSession(ctx.author.id)
                ttsSessions[session.guid] = session
                print(ttsSessions)
                vc = await voice_channel.connect()
                session.isTTSEnabled = True
                session.voice_channel = vc
            else:
                await ctx.send(f'{str(ctx.author.name)} is not in a channel(VCに入ってくださいね~!)')
            await ctx.send(f'やっほ~ >_<)9')
        except AttributeError:
            print('AttributeError')
            await ctx.send(f'{str(ctx.author.name)} is not in a channel(VCに入ってくださいね~!)')
    else:
        # Remove TTSSession
        sessionKey = find_sessionKey(ctx)
        
        if(sessionKey != None):
            # Leave voice chat
            session : TTSSession = ttsSessions[sessionKey]
            await session.voice_channel.disconnect()

            wavpath = f'{session.guid}.wav'
            if (os.path.exists(wavpath)):
                os.remove(wavpath)
            else:
                print(f'Cannot remove the file {wavpath}')
            session.isTTSEnabled = False
            del ttsSessions[sessionKey]
            print(ttsSessions)
            await ctx.send(f'またね~!')

@bot.event
async def on_message(message):
    chat = message.content
    print(f'author: {message.author}, chat: {chat}')
    if (message.author != bot.user):
        if(chat[0] == '!'):
            await bot.process_commands(message)
        else:
            ctx = await bot.get_context(message)
            sessionKey = find_sessionKey(ctx)
            if(sessionKey != None):
                session = ttsSessions[sessionKey]
                if(session.isTTSEnabled):
                    # message.content = f'!sayf {chat}'
                    message.content = f'!say {chat}'
                    await bot.process_commands(message)

apikey = settings['bot2_api_token']
bot.run(apikey)
