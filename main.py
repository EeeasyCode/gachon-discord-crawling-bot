import crawling.get_notice
from crawling import academic_calender
import discord
from discord.ext import commands
import config

app = commands.Bot(command_prefix='!')


@app.event
async def on_ready():
    print('Logged in as')
    print(app.user.name)
    print(app.user.id)
    print('------')


@app.command(name='학사공지')
async def notice(ctx):
    notice_list, date_list = crawling.get_notice.get_notice()
    embed = discord.Embed(title="가천대학교 공지사항", description="")
    for i in range(len(notice_list)):
        embed.add_field(name="제목", value=notice_list[i])
        embed.add_field(name="작성일", value=date_list[
                                              i] + "\n------------------------------------------------------------------------------",
                        inline=False)
    await ctx.send(embed=embed)


@app.command(name="학사일정")
async def calender(ctx, month):
    dates, contents = academic_calender.Academic_calender(month)
    embed = discord.Embed(title="가천대학교 학사일정", description="2022년 " + month + " 학사일정")
    embed.add_field(name="기간", value='\n'.join(dates))
    embed.add_field(name="일정", value='\n'.join(contents))

    await ctx.send(embed=embed)


app.run(config.DISCORD_CONFIG['token'])





