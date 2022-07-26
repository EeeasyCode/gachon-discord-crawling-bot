import academic_calender
import discord
import requests
from bs4 import BeautifulSoup
import config

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
        url = "https://www.gachon.ac.kr/kor/3104/subview.do"
        response = requests.get(url)
        if response.status_code == 200:
            embed = discord.Embed(title="가천대학교 공지사항", description="")
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            notices_table = soup.select('table > tbody > tr > td.td-subject > a > strong')
            date_table = soup.select('table > tbody > tr > td.td-date')

            notice_list = [notice.get_text() for notice in notices_table]
            date_list = [dates.get_text() for dates in date_table]

            for i in range(len(notice_list)):
                embed.add_field(name="제목", value=notice_list[i])
                embed.add_field(name="작성일", value=date_list[i] + "\n------------------------------------------------------------------------------",
                                inline=False)
        else:
            print(response.status_code)
        await message.channel.send(embed=embed)

    elif message.content.startswith('!학사일정'):
        await message.channel.send(academic_calender.Academic_calender())
    elif message.content.startswith('!안녕'):
        await message.channel.send("안녕 ㅎㅎ")


client.run(config.DISCORD_CONFIG['token'])
