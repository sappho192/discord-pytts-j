# discord-pytts-j
Discord Japanese TTS bot based on OpenJTalk and Flask

# Requirements
- Python 3.8.8 (recommended) or above
- Linux(Debian, Ubuntu) recommended

## 1. TTS Server
- Flask (`pip install flask`)
- OpenJTalk [[Setup Instruction](https://thr3a.hatenablog.com/entry/20180223/1519360909)]

## 2. TTS Bot
- Discord.py, PyNaCl (`pip install discord pynacl`)
- **(IMPORTANT) Turn on "SERVER MEMBERS INTENT" in your Discord Bot settings** [[Check here](https://support.discord.com/hc/en-us/articles/360040720412#privileged-intent-whitelisting)]

# Setup instruction
1. Install requirements stated above
1. Create `settings.json` by cloning `settings-default.json`
1. Replace `bot_api_token` and `tts_api_endpoint` to your own data

# Execute instruction (How to use)
## 1. TTS Server (main.py)
- Enter following command in Linux terminal
`nohup python main.py > tts.log &`

## 2. TTS Bot (bot.py)
- Enter following command in Linux terminal
`nohup python bot.py > bot.log &`

- You can also run other bots with following command
- To run 2nd bot, replace `bot2_api_token` in settings.json
`nohup python bot2.py > bot2.log &`
- To run 3rd bot, replace `bot3_api_token` in settings.json
`nohup python bot3.py > bot3.log &`

