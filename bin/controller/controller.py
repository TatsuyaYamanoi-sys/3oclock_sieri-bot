import logging
import os
from pathlib import Path
import re
import sys

from dotenv import load_dotenv
import discord

if '../' not in sys.path:
    sys.path.append('../')  # 同階層の読み込みに必須
import controller.compatibility
# import controller.functions

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOTENV_PATH = os.path.join(BASE_DIR, '.env')
print(DOTENV_PATH)
load_dotenv(DOTENV_PATH)
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
# TOKEN = os.environ.get("TEST_TOKEN")    # <- debug

### log ###
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if client.user != message.author and not message.author.bot:
        # print('clientuser = ', client.user)
        # print('messageouthor = ', message.author)
        # print('msgcontent = ', str(message.content))
        # print('re result = ', re.search(r'.+$', message.content))
        if message.content.startswith('/相性'):
            logger.info({
                'action': 'on_message: 相性',
                'status': 'run'
            })
            compa = controller.compatibility.Compatibility()
            if re.search(r',.+', message.content):
                logger.info({
                    'action': 'on_message: 相性, any',
                    'status': 'run'
                })
                input_cmd = [c.strip() for c in message.content.split(',')]
                msg = compa.get_compatibility_msg(input_cmd)
                logger.info({
                    'action': 'on_message: 相性, any',
                    'status': 'success'
                })
            else:
                msg = compa.msg
            
            await message.channel.send(msg)
            logger.info({
                'action': 'on_message: 相性',
                'status': 'success'
            })
            
        elif message.content.startswith('気を付けて帰ってね') or message.content.startswith('きをつけてかえってね'):
            await message.channel.send('やさしお (ーqー)')
        else:
            logger.info({
                'action': 'on_message: else',
                'status': 'run'
            })
            # ポケモン名でデータ取得
            # name, diffence_type, attack_type, next_stage_level
            pass
