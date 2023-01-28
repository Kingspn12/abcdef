from os import environ
import os
import time
from urllib.request import urlopen
from urllib.parse import urlparse
import aiohttp
from pyrogram import Client, filters
from pyshorteners 
from bs4 import BeautifulSoup
from doodstream import DoodStream
import requests
import re

API_ID = environ.get('26871269')
API_HASH = environ.get('c49f273ffa27f53f7751557950b4c8c9')
BOT_TOKEN = environ.get('5787420184:AAEr_UQnpBbQHXeOnYv2NyDjEGXPPxqZlzE')
DOODSTREAM_API_KEY = environ.get('169472plyqdcv9srcis3qm')
bot = Client('Doodstream bot',
             api_id=API_ID,
             api_hash=API_HASH,
             bot_token=BOT_TOKEN,
             workers=50,
             sleep_threshold=0)


@bot.on_message(filters.command('start') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**I am a Mdisk/Doodstream post convertor bot and i am able to upload all direct links to Mdisk/Doodstream,just send me links or full post... \n Join my Group @ComicBank**")

@bot.on_message(filters.command('help') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hello, {message.chat.first_name}!**\n\n"
        "**If you send post which had Mdisk/Doodstream Links, texts & images... Than I'll convert & replace all Mdisk/Doodstream links with your Mdisk/Doodstream links \nMessage me @kamdev07 For more help-**")

@bot.on_message(filters.command('support') & filters.private)
async def start(bot, message):
    await message.reply(
        f"**Hey, {message.chat.first_name}!**\n\n"
        "**please contact me on @kamdev07 or for more join @Doodstream_Admins**")
    
@bot.on_message(filters.text & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.text)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
        await message.reply(f'{Doodstream_link}' , quote=True)
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)


@bot.on_message(filters.photo & filters.private)
async def Doodstream_uploader(bot, message):
    new_string = str(message.caption)
    conv = await message.reply("Converting...")
    dele = conv["message_id"]
    try:
        Doodstream_link = await multi_Doodstream_up(new_string)
        if(len(Doodstream_link) > 1020):
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await message.reply(f'{Doodstream_link}' , quote=True)
        else:
            await bot.delete_messages(chat_id=message.chat.id, message_ids=dele)
            await bot.send_photo(message.chat.id, message.photo.file_id, caption=f'{Doodstream_link}')
    except Exception as e:
        await message.reply(f'Error: {e}', quote=True)



async def Doodstream_up(links):
    if ('bit' in links ):
        #links = urlopen(links).geturl()
        unshortener = UnshortenIt()
        links = unshortener.unshorten(links)
    if ('dood'in links ):
        title_new = urlparse(links)
        title_new = os.path.basename(title_new.path)
        title_Doodstream = '@' + CHANNEL + title_new
        res = requests.get(
             f'https://doodapi.com/api/upload/url?key={DOODSTREAM_API_KEY}&url={links}&new_title={title_Doodstream}')
         
        data = res.json()
        data = dict(data)
        print(data)
        v_id = data['result']['filecode']
        #bot.delete_messages(con)
        v_url = 'https://dood.la/d/' + v_id
 
    
async def multi_Doodstream_up(ml_string):
    list_string = ml_string.splitlines()
    ml_string = ' \n'.join(list_string)
    new_ml_string = list(map(str, ml_string.split(" ")))
    new_ml_string = await remove_username(new_ml_string)
    new_join_str = "".join(new_ml_string)

    urls = re.findall(r'(https?://[^\s]+)', new_join_str)

    nml_len = len(new_ml_string)
    u_len = len(urls)
    url_index = []
    count = 0
    for i in range(nml_len):
        for j in range(u_len):
            if (urls[j] in new_ml_string[i]):
                url_index.append(count)
        count += 1
    new_urls = await new_Doodstream_url(urls)
    url_index = list(dict.fromkeys(url_index))
    i = 0
    for j in url_index:
        new_ml_string[j] = new_ml_string[j].replace(urls[i], new_urls[i])
        i += 1

    new_string = " ".join(new_ml_string)
    return await addFooter(new_string)


async def new_Doodstream_url(urls):
    new_urls = []
    for i in urls:
        #if ('entertainvideo' in urls or 'mdisk' in urls or 'bit' in urls or 'bit' in urls):
        time.sleep(0.2)
        new_urls.append(await Doodstream_up(i))
        #else:
            #continue
    return new_urls




async def addFooter(str):
    footer = """
    ━━━━━━━━━━━━━━━
⚙️ How to Download / Watch Online :""" + HOWTO + """
━━━━━━━━━━━━━━━
⭐️JOIN CHANNEL ➡️ t.me/""" + CHANNEL
    return str + footer

bot.run()
