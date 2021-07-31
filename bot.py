# Japanese TTS bot
# You should install discord and pynacl package with pip

import discord
from discord.ext.commands import Bot
from urllib import request, parse
from time import sleep
import json

intents = discord.Intents.default()
bot = Bot(command_prefix='!', intents=intents)
global settings
with open('settings.json', 'r') as file:
    settings = json.load(file)
print(json.dumps(settings))

@bot.event
async def on_ready():
    print(f'logged in to {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

@bot.command()
async def sayf(ctx, arg):
    encoded = parse.quote(str(arg))
    endpoint = settings['tts_api_endpoint']
    url = f'{endpoint}{encoded}'
    print(f'url:{url}')
    filepath = 'tts.wav'
    request.urlretrieve(url, filepath)
    await ctx.send(file=discord.File(filepath))
    # await ctx.send(f'{str(arg)}!')

@bot.command()
async def say(ctx, arg):
    encoded = parse.quote(str(arg))
    endpoint = settings['tts_api_endpoint']
    url = f'{endpoint}{encoded}'
    filepath = 'tts.wav'
    request.urlretrieve(url, filepath)
    
    try:
        voice_channel = ctx.author.voice.channel
        channel = None
        if voice_channel != None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio(source=filepath))
            while vc.is_playing():
                sleep(.1)
            await vc.disconnect()
        else:
            await ctx.send(f'{str(ctx.author.name)} is not in a channel')
        # await ctx.message.delete()
    except AttributeError:
        return # skips when the user is not in voice

ttsEnabled = False
@bot.command()
async def tts(ctx):
    global ttsEnabled
    if(not ttsEnabled):
        ttsEnabled = True
        await ctx.send(f'tts is enabled')
    else:
        ttsEnabled = False
        await ctx.send(f'tts is disabled')

@bot.event
async def on_message(message):
    chat = message.content
    print(f'{chat}')
    if (message.author != bot.user):
        if(chat[0] == '!'):
            await bot.process_commands(message)
        else:
            if(ttsEnabled):
                message.content = f'!sayf {chat}'
                await bot.process_commands(message)

apikey = settings['bot_api_token']
bot.run(apikey)
