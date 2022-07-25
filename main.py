import discord
import requests
from bs4 import BeautifulSoup
from html_table_parser import parser_functions as parser
import pandas as pd
import config

def get_notice():
    url = "https://www.gachon.ac.kr/kor/3104/subview.do"

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        target = soup.find_all('table')
        p = parser.make2d(target[0])
        df = pd.DataFrame([p[i][1] for i in range(1, 14)])
        return df

    else:
        print(response.status_code)


client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!학사공지'):
        await message.channel.send(get_notice())
    elif message.content.startswith('!반가워요'):
        await message.channel.send('저도 반가워요.')


client.run(config.DISCORD_CONFIG['token'])
