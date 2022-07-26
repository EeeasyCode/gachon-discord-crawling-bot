import crawling.get_notice
from apis import bus, sub
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


@app.command(name="지하철")
async def subway(ctx, way):
    first_sub_data, second_sub_data = sub.subway(way)
    embed = discord.Embed(title="가천대역 지하철 정보", description=first_sub_data['recptnDt'] + "기준")
    embed.add_field(name="종점 - 방면", value=first_sub_data['trainLineNm'] + '\n' + second_sub_data['trainLineNm'])
    embed.add_field(name="도착 여부", value=first_sub_data['arvlMsg2'] + '\n' + second_sub_data['arvlMsg2'])
    await ctx.send(embed=embed)


@app.command(name="버스")
async def busInfo(ctx, stationName):
    busNo, busEndStart, busLocation, locationNo1, locationNo2, predictTime1, predictTime2, remainSeatCnt1, remainSeatCnt2 = bus.gachon_bus(
        stationName)

    for i in range(0, 13):
        embed = discord.Embed(title="가천대 버스 도착 정보", description=stationName)
        embed.add_field(name=busNo[i] + " " + busLocation[i][0], value='------------------------------', inline=False)
        embed.add_field(name='경유정보', value=busEndStart[i], inline=False)
        if predictTime1[i] is None or locationNo1[i] is None or remainSeatCnt1[i] is None:
            embed.add_field(name='첫번째', value='배차정보가 없습니다')
        else:
            embed.add_field(name='첫번째',
                            value=predictTime1[i] + '분 ' + locationNo1[i] + '정류장/' + remainSeatCnt1[i] + '석')
        if predictTime2[i] is None or locationNo2[i] is None or remainSeatCnt2[i] is None:
            embed.add_field(name='두번째', value="배차정보가 없습니다.")
        else:
            embed.add_field(name='두번째',
                            value=predictTime2[i] + '분 ' + locationNo2[i] + '정류장/' + remainSeatCnt2[i] + '석')
        await ctx.send(embed=embed)


app.run(config.DISCORD_CONFIG['token'])

# # seoul_bus_url = "http://ws.bus.go.kr/api/rest/stationinfo/getStationByUid"
# # seoul_bus_params = {
# #     'serviceKey': config.BUS_CONFIG['service-key'],
# #     'arsId': arsID
# # }
# # seoul_bus_response = requests.get(seoul_bus_url, params=seoul_bus_params)
# # print(seoul_bus_response.text)

