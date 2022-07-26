import discord
import config
import academic_calender as calender
import get_notice as notice

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
        await message.channel.send(notice.get_notice())
    elif message.content.startswith('!학사일정'):
        await message.channel.send(calender.Academic_calender())
    elif message.content.startswith('!안녕'):
        await message.channel.send("안녕 ㅎㅎ")


client.run(config.DISCORD_CONFIG['token'])
