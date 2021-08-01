# Japanese TTS bot
# You should install discord and pynacl package with pip

import discord
from discord.ext.commands import Bot
from urllib import request, parse
from time import sleep
import json
from datetime import datetime
import os
import hashlib

intents = discord.Intents.default()
intents.voice_states = True
intents.members = True
intents.guilds = True
bot = Bot(command_prefix='!', intents=intents)
global settings
with open('settings.json', 'r') as file:
    settings = json.load(file)
print(json.dumps(settings))

class TTSSession:
    def __init__(self, voice_channel, text_channel):
        date = datetime.now()
        timestamp = date.strftime("%Y-%b-%d-%H-%M-%S-%f")
        self.voice_channel = voice_channel
        self.text_channel = text_channel
        print(f'tc: {str(text_channel.id)}')
        enc = hashlib.md5()
        enc.update(repr(text_channel.id).encode())
        ustr = f'{enc.hexdigest()}_{timestamp}'
        print(f'ustr: {ustr}')
        self.guid = ustr
        print(f'uid created: {self.guid}')
        self.isTTSEnabled = False

global ttsSessions
ttsSessions = dict()

def find_sessionKey(ctx):
        sessionKey = None
        for key in ttsSessions:
            text_channel = ttsSessions[key].text_channel
            if (text_channel.id == ctx.channel.id):
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
async def tts(ctx):
    session : TTSSession = find_sessionKey(ctx)
    if(session == None):
        # Join voice chat
        try:
            print('Joining voice chat')
            voice_channel = ctx.author.voice.channel
            if voice_channel != None:
                # Create TTSSession
                print('Creating new session')
                session = TTSSession(voice_channel, ctx.channel)
                ttsSessions[session.guid] = session
                print(ttsSessions)
                vc = await voice_channel.connect()
                session.isTTSEnabled = True
                session.voice_channel = vc
            else:
                await ctx.send(f'VCに入ってくださいね~!')
            await ctx.send(f'やっほ~ >_<)9')
        except AttributeError as e:
            print(e)
            await ctx.send(f'VCに入ってくださいね~!')
    else:
        # Remove TTSSession
        sessionKey = find_sessionKey(ctx)
        
        try:
            voice_channel = ctx.author.voice.channel
            if voice_channel != None:
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
            else:
                await ctx.send(f'VCに入ってくださいね~!')
        except AttributeError as e:
            print(e)
            await ctx.send(f'VCに入ってくださいね~!')

@bot.event
async def on_message(message):
    chat = message.content
    print(f'author: {message.author}, chat: {chat}')
    msgclient = message.guild.voice_client
    if message.content.startswith('!'):
        await bot.process_commands(message)
    else:
        if message.guild.voice_client:
            print(message.content)
            ctx = await bot.get_context(message)
            sessionKey = find_sessionKey(ctx)
            if(sessionKey != None):
                session = ttsSessions[sessionKey]
                if(session.isTTSEnabled):
                    # message.content = f'!sayf {chat}'
                    message.content = f'!say {chat}'
                    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is not None and len(voice_state.channel.members) == 1:
        await voice_state.disconnect()

apikey = settings['bot3_api_token']
bot.run(apikey)
