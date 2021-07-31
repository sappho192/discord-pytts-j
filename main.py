# OpenJTalk-based TTS server
# Install and setup OpenJTalk with referring following blog:
# https://thr3a.hatenablog.com/entry/20180223/1519360909

import os, sys
from flask import Flask, send_file
app = Flask (__name__)

@app.route('/')
def hello_world():
    return 'TTS api starts with /api/tts/<Japanese sentence>'

@app.route('/api/tts/<sentence>')
def tts(sentence):
    command = f'echo \'{sentence}\' | open_jtalk -x /var/lib/mecab/dic/open-jtalk/naist-jdic -m /usr/share/hts-voice/mei/mei_normal.htsvoice -r 1.0 -ow test.wav'
    os.system(command)
    # return f'You said {sentence}'
    return send_file('test.wav')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=30000)
