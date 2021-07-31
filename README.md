# pytts
Discord Japanese TTS bot based on OpenJTalk and Flask

# Requirements
- Python 3.8.8 or above
- Linux(Debian, Ubuntu) recommended

## TTS Server
- Flask (`pip install flask`)
- OpenJTalk [[Setup Instruction](https://thr3a.hatenablog.com/entry/20180223/1519360909)]

## TTS Bot
- Discord.py, PyNaCl (`pip install discord pynacl`)

## Setup instruction
1. Install requirements stated above
1. Create `settings.json` by cloning `settings-default.json`
1. Replace `bot_api_token` and `tts_api_endpoint` to your own data

## Execute instruction
### TTS Server (main.py)
- Enter following command in Linux terminal
`nohup python main.py > tts.log &`

### TTS Bot (bot.py)
- Enter following command in Linux terminal
`nohup python bot.py > bot.log &`

