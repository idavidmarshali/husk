import discord
from discord.ext import commands
import time
import json
import webcolors
import requests
import binascii
import asyncio
import random
from itertools import cycle

t = time.strftime('%H:%M:%S', time.localtime())
prefix = '!!'

## logger stat checker
def logger_stat_checker(server_id):
    try:
        with open('./servers.json', 'r') as file:
            data = json.load(file)
    except json.decoder.JSONDecodeError:
        print('logger stat check error')
    if f'{server_id}' in data['servers']:
        if data['servers'][f'{server_id}']["log_stat"] == 'off':
            return False, 'False'
        elif data['servers'][f'{server_id}']["log_stat"] == 'on':
            return True, data['servers'][f'{server_id}']['log_channel']
    else:
        return False, 'False'



def moverage_checker(server_id):
    with open('./servers.json') as file:
        data = json.load(file)
    if f'{server_id}' in data['servers']:
        place = data['servers'][f'{server_id}']
        if place['moverage_channel1'] != 'None' and place['moverage_channel2'] == 'None':
            return [place['moverage_channel1']]
        elif place['moverage_channel2'] != 'None' and place['moverage_channel1'] == 'None':
            return [place['moverage_channel2']]
        elif place['moverage_channel1'] != 'None' and place['moverage_channel2'] != 'None':
            return place['moverage_channel1'], place['moverage_channel2']
        elif place['moverage_channel1'] == 'None' and place['moverage_channel2'] == 'None':
            return []
    return []

# wait for checker
def check(author):
    def inner_check(message):
        if message.author != author:
            return False
        try:
            return message.content
        except ValueError:
            return False
    return inner_check


def to_hex(str: str):
    string = binascii.hexlify(str.encode())
    return string.decode()


def from_hex(str: str):
    string = binascii.unhexlify(str).decode()
    return string



class Maincommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    # Command zone------------↴
    @commands.has_guild_permissions(move_members=True)
    @commands.command()
    async def moveall(self, message):
        guild = message.guild
        move_clients = []
        for vchannel in guild.voice_channels:
            member = list(vchannel.voice_states)
            if member != []:
                for x in member:
                    move_clients.append(x)
        moved_mmbers = []
        for member in move_clients:
            user = message.guild.get_member(member)
            moved_mmbers.append(f'├`{user.name}`\n')
            await user.move_to(message.author.voice.channel)

        embed = discord.Embed(title="Moved Users :", description="┌-----------↴", color=discord.Color.random())
        embed.add_field(name=f"{''.join(moved_mmbers)}", value='└-----------⬏', inline=False)
        embed.add_field(name="Target Channel :", value=f"`{message.author.voice.channel}`")
        await message.send(embed=embed)

    @commands.has_guild_permissions(manage_messages=True)
    @commands.command(aliases=['del', 'clear', 'delete', 'clearchat', 'cl'])
    async def chatclear(self, message, arg=5):
        await message.message.delete()
        if arg < 100:
            await message.channel.purge(limit=arg)
            x = await message.send(
                f"**clear Command** | `🛑` `{arg} Messages has been deleted in {message.channel} at {t}`")
            time.sleep(3)
            await x.delete()
            log_stat = logger_stat_checker(message.guild.id)
            if log_stat[0]:
                channel = self.bot.get_channel(log_stat[1])
                await channel.send(
                    f"**TC** | **clear Command** : `🛑` `{arg} Messages has been deleted in {message.channel} at {t} by "
                    f"{message.author.name}`")
        else:
            x = await message.send(f"**clear Command** | `🚫` `You requested {arg}, but max allowed is 100!!`")
            time.sleep(3)
            await x.delete()



    @commands.has_guild_permissions(move_members=True)
    @commands.command()
    async def moverage(self, message, member: discord.Member, chan1=None, chan2=None):
                check = moverage_checker(message.guild.id)
                lenght = len(check)
                limit = 5
                await message.message.delete()
                if chan1 is None and chan2 is None:
                    if lenght < 2:
                        await message.send(
                            f"**MOVERAGE** | `⚠` `ERROR!!, You didnt input any channels and the server doesn't "
                            f"have enough preassigned MoveRage VoiceChannels!, pls use` `!!help moverage` `For "
                            f"more Info`")
                    elif lenght == 2:
                        channel1 = self.bot.get_channel(check[0])
                        channel2 = self.bot.get_channel(check[1])
                        for x in range(0, limit):
                            await member.move_to(channel1)
                            time.sleep(0.3)
                            await member.move_to(channel2)
                        await message.send(
                            f'**MOVERAGE** | `⚠` `{member.name} has been Ragely Moved by {message.author.name} '
                            f'request!!`')
                        log = logger_stat_checker(message.guild.id)
                        if log[0] == True:
                            await self.bot.get_channel(log[1]).send(
                                f'**MOVERAGE** | `⚠` `{member.name} has been Ragely Moved by {message.author.name} '
                                f'request at {t}!!`')
                elif chan1 is None and chan2 is not None:
                     if self.bot.get_channel(chan2)==None:
                         await message.send(
                             f'**MOVERAGE** | `⚠` `Channel Input is not valid!!`')
                     else:
                        if lenght == 0:
                            await message.send(
                                f"**MOVERAGE** | `⚠` `ERROR!!, You have inputted one channel but the server has no "
                                f"preassigned MoveRage VoiceChannels!, pls use ``!!help moverage` ` For more Info!`")
                        else:
                            channel1 = self.bot.get_channel(check[0])
                            channel2 = self.bot.get_channel(int(chan2))
                            for x in range(0, limit):
                                await member.move_to(channel2)
                                time.sleep(0.3)
                                await member.move_to(channel1)
                            await message.send(
                                f'**MOVERAGE** | `⚠` `{member.name} has been Ragely Moved by {message.author.name} '
                                f'request!!`')
                            log = logger_stat_checker(message.guild.id)
                            if log[0] == True:
                                await self.bot.get_channel(log[1]).send(
                                    f'**MOVERAGE** | `⚠` `{member.name} has been Ragely Moved by {message.author.name} '
                                    f'request at {t}!!`')

                elif chan2 is None and chan1 is not None:
                    if self.bot.get_channel(chan1) == None:
                        await message.send(
                            f'**MOVERAGE** | `⚠` `Channel Input is not valid!!`')
                    else:
                        if lenght == 0:
                            await message.send(
                                f"**MOVERAGE** | `⚠` `ERROR!!, You have inputted one channel but the server has no "
                                f"preassigned MoveRage VoiceChannels!, pls use ``!!help moverage` ` For more Info!`")
                        else:
                            channel1 = self.bot.get_channel(check[0])
                            channel2 = self.bot.get_channel(int(chan1))
                            for x in range(0, limit):
                                await member.move_to(channel2)
                                time.sleep(0.3)
                                await member.move_to(channel1)
                            await message.send(
                                f'**MOVERAGE** | `⚠` `{member.name} has been Ragely Moved by {message.author.name} '
                                f'request!!`')
                            log = logger_stat_checker(message.guild.id)
                            if log[0] == True:
                                await self.bot.get_channel(log[1]).send(
                                    f'**MOVERAGE** | `⚠` `{member.name} has been Ragely Moved by {message.author.name} '
                                    f'request at {t}!!`')

                elif chan2 is not None and chan1 is not None:
                    if self.bot.get_channel(chan2) == None or self.bot.get_channel(chan1)==None:
                            await message.send(
                                f'**MOVERAGE** | `⚠` `one or both of your Channel Inputs are invalid!!`')
                    else:
                        channel1 = self.bot.get_channel(int(chan1))
                        channel2 = self.bot.get_channel(int(chan2))
                        for x in range(0, limit):
                            await member.move_to(channel2)
                            time.sleep(0.3)
                            await member.move_to(channel1)
                        await message.send(
                            f'**MOVERAGE** | `⚠` `{member.name} has been Ragely Moved by {message.author.name} request!!`')
                        log = logger_stat_checker(message.guild.id)
                        if log[0] == True:
                            await self.bot.get_channel(log[1]).send(
                                f'**MOVERAGE** | `⚠` `{member.name} has been Ragely Moved by {message.author.name} '
                                f'request at {t}!!`')

    @commands.has_guild_permissions(mute_members=True)
    @commands.command()
    async def muteall(self,message):
        members = message.author.voice.channel.members
        names = []
        for m in members:
            await m.edit(mute=True)
            names.append(f'├`{m.name}`\n')
        embed = discord.Embed(title="Muted Users :", description="┌-----------↴", color=discord.Color.random())
        embed.add_field(name=f"{''.join(names)}", value='└-----------⬏', inline=False)
        embed.add_field(name="Muted Channel :", value=f"`{message.author.voice.channel}`")
        await message.send(embed=embed)
        x = logger_stat_checker(message.guild.id)
        if x[0]:
            channel = self.bot.get_channel(x[1])
            await channel.send(
                f'**MOD** | `⚠` `Muteall command, requested by {message.author.name} in {message.author.voice.channel}, '
                f'at {t}`')

    @commands.has_guild_permissions(mute_members=True)
    @commands.command()
    async def unmuteall(self,message):
        members = message.author.voice.channel.members
        names = []
        log = []
        for m in members:
            await m.edit(mute=False)
            names.append(f'├`{m.name}`\n')
            log.append(f'`{m.name}`')
        embed = discord.Embed(title="UNMuted Users :", description="┌-----------↴", color=discord.Color.random())
        embed.add_field(name=f"{''.join(names)}", value='└-----------⬏', inline=False)
        embed.add_field(name="UNMuted Channel :", value=f"`{message.author.voice.channel}`")
        await message.send(embed=embed)
        x = logger_stat_checker(message.guild.id)
        if x[0]:
            channel = self.bot.get_channel(x[1])
            await channel.send(f'**MOD** | `⚠` `UnMuteall command, requested by {message.author.name} in '
                               f'{message.author.voice.channel}, at {t}`')


    @commands.command(aliases=['user', 'info'])
    async def check(self,message, user : discord.User):
        member: discord.Member = discord.utils.get(message.guild.members, id=user.id)
        def premium(mem: discord.Member):
            if mem.premium_since != None:
                return f'Boosting Since : {mem.premium_since}'
            else:
                return 'No'
        date = user.created_at.strftime('%Y-%m-%d')
        time = user.created_at.strftime('%H:%M:%S')
        try:

            color_web = webcolors.name_to_rgb(f'{user.default_avatar}')
            color = discord.Colour.from_rgb(color_web.red, color_web.green, color_web.blue)
        except ValueError:
            color = discord.Color.random()
        embed = discord.Embed(title=f"User's DisplayName: `{user.display_name}`",
                              description=f"**User's id** : `{user.id}`\n"
                                          f"**User's Discriminator** : `#{user.discriminator}`",
                              color=color)
        embed.set_author(name="Husk User Checker")
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=f'{prefix}check - exec at {t} - by {message.author}', )
        embed.add_field(name=f"**Account Created in** `{date}` **at** `{time}`",
                        value=f"**Profile avatar** : [Click]({user.avatar_url})\n"
                              f"**Is Boosting server?** : `{premium(member)}`\n"
                              f"**Animated Profile Avatar?** : `{user.is_avatar_animated()}`\n"
                              f"**is a Bot?** : `{user.bot}`\n"
                              f"**Default Avatar** : [Click]({user.default_avatar_url})\n"
                              f"**Default Avatar Color** : `{user.default_avatar}`\n"
                              f"**Currently in**: `{member.activity}\n`"
                              f"**is on mobile?** : `{member.is_on_mobile()}\n`"
                              f"**Status** : `{member.status}\n`",

                        inline=False)
        await message.send(embed=embed)

    @commands.command(aliases=['bug'])
    async def report(self, message,*,bug):
        with open('./bot.json','r') as file:
            data = json.load(file)
            moderator: discord.Member = discord.utils.get(message.guild.members, id=data['bot']['moderator'])
            mod_chan = await moderator.create_dm()
            await mod_chan.send(f'```diff\n+{message.author}\n-server : {message.guild} | {message.guild.id}``````diff'
                                f'\n-message: \n {bug}```')
        await message.send('**report successful**', delete_after=5)
        await message.message.delete()


    @commands.has_guild_permissions(ban_members=True)
    @commands.command()
    async def ban(self, message, member : discord.Member, *,reason=None):
        member_name = member.display_name
        await member.ban(reason=reason)
        x = await message.send(f"**MOD** | **`{member_name}` has been banned from `{message.guild}` at `{t}` with "
                               f"`{message.author}'s` Request**.\n **Reason** : `{reason}`  ")
        log = logger_stat_checker(message.guild.id)[0]
        if log[0]:
            channel = self.bot.get_channel(log[1])
            await channel.send(f"**MOD** | **`{member_name}` has been banned from `{message.guild}` at `{t}` with "
                               f"`{message.author}'s` Request**.\n **Reason** : `{reason}`  ")
        time.sleep(5)
        await x.delete()
        await message.message.delete()
    @commands.has_guild_permissions(kick_members=True)
    @commands.command()
    async def kick(self, message, member: discord.Member, *,reason=None):
        member_name = member.display_name
        await member.kick(reason=reason)
        x = await message.send(f"**MOD** | **`{member_name}` has been kicked from `{message.guild}` at `{t}` with "
                               f"`{message.author}'s` Request**.\n **Reason** : `{reason}`  ")

        log = logger_stat_checker(message.guild.id)[0]
        if log[0]:
            channel = self.bot.get_channel(log[1])
            await channel.send(f"**MOD** | **`{member_name}` has been banned from `{message.guild}` at `{t}` with "
                               f"`{message.author}'s` Request**.\n **Reason** : `{reason}`  ")
        time.sleep(5)
        await x.delete()
        await message.message.delete()
    @commands.command(aliases=['gimme'])
    async def meme(self,message):
        wait_msg = await message.send(f'**Retrieving Data** ')
        try:
            respond = requests.api.get('https://meme-api.herokuapp.com/gimme')
            if respond.status_code == 200:
                data = respond.json()
                embed = discord.Embed(title=discord.Embed.Empty,
                                      description=discord.Embed.Empty,
                                      color=discord.colour.Color.dark_orange())
                embed.set_author(name=f"{data['title']}", url=data['postLink'],
                                 icon_url='https://2.bp.blogspot.com/-r3brlD_9eHg/XDz5bERnBMI/AAAAAAAAG2Y/XfivK0eVkiQej2t-xfmlNL6MlSQZkvcEACK4BGAYYCw/s1600/logo%2Breddit.png')
                embed.set_image(url=data['url'])
                embed.set_footer(
                    text=f'⬆ UpVotes : {data["ups"]} , subreddit : {data["subreddit"]},\n 🔞 NSFW : {data["nsfw"]}, ✍author : {data["author"]}')
                await wait_msg.edit(content=None, embed=embed)
            else:
                await wait_msg.edit(content=f'**Failed, Respond Code : `{respond.status_code}`**')
        except requests.exceptions.ConnectionError:
            await wait_msg.edit(content=f'**Connection Error, Try Again**', delete_after=5)
            await message.message.delete()


    @commands.command()
    async def subreddit(self, message, arg):
        def embed_msg(data):
            embed = discord.Embed(title=discord.Embed.Empty,
                                  description=discord.Embed.Empty,
                                  color=discord.colour.Color.dark_orange())
            embed.set_author(name=f"{data['title']}", url=data['postLink'],
                             icon_url='https://2.bp.blogspot.com/-r3brlD_9eHg/XDz5bERnBMI/AAAAAAAAG2Y/XfivK0eVkiQej2t-xfmlNL6MlSQZkvcEACK4BGAYYCw/s1600/logo%2Breddit.png')
            embed.set_image(url=data['url'])
            embed.set_footer(
                text=f'⬆ UpVotes : {data["ups"]} , subreddit : {data["subreddit"]},\n 🔞 NSFW : {data["nsfw"]}, ✍author : {data["author"]}')
            return embed
        r = requests.api.get(f'https://meme-api.herokuapp.com/gimme/{arg}')
        if r.status_code == 200:
            data = r.json()
            if data['nsfw']:
                if message.channel.is_nsfw():
                    await message.send(embed=embed_msg(data))
                else:
                    x  = await message.send(f'**NSFW** | `🔞` `{message.channel} is not an NSFW channel!`')
                    time.sleep(3)
                    await x.delete()
                    await message.message.delete()
            else:
                await message.send(embed=embed_msg(data))
        else:
            await message.send(f'**REDDIT ERROR** | `🚫` `{r.json()}`', delete_after=5)
            await message.message.delete()


    @commands.command()
    async def hex(self, message):
        embed = discord.Embed(title=discord.Embed.Empty, description='╔ `1- Encode To hex`\n'
                                                                     '╠ `2- Decode From hex`\n'
                                                                     '╚ `3- Cancel`\n**Send me the number**',
                              color=0x0000)
        embed.set_author(name='*Wich operation do you want to do*?',
                         icon_url='https://img.icons8.com/color/452/hexadecimal.png')
        y = await message.send(embed=embed)
        await message.message.delete()
        first_reply = await self.bot.wait_for('message', check=check(message.author), timeout=30)
        if first_reply.content == '1':
            await first_reply.delete()
            await y.edit(content='**send me the `text` that you wish to hexlify!!**', suppress=True)
            second_reply = await self.bot.wait_for('message', check=check(message.author), timeout=30)
            hex_text = to_hex(second_reply.content)
            await y.edit(content=f'**your `hex` string is :**\n```json\n"{hex_text}"```', suppress=True,
                         delete_after=30)
            await second_reply.delete()
        elif first_reply.content=='2':
            await first_reply.delete()
            await y.edit(content='**send me the `hex-encoded-text` that you wish to turn back!!**', suppress=True)
            second_reply = await self.bot.wait_for('message', check=check(message.author), timeout=30)
            ascii_text = from_hex(second_reply.content)
            await y.edit(content=f'**your `ascii` string is :**\n```json\n"{ascii_text}"```', suppress=True,
                         delete_after=30)
            await second_reply.delete()
        elif first_reply.content=='3':
            await y.edit(content='`hex Menu` **Canceled**', suppress=True, delete_after=5)
            await first_reply.delete()
        else:
            await y.edit(content='**ERROR** | `🛑` `Wrong input!! pls respond with a valid input.`', suppress=True,
                         delete_after=5)
            await asyncio.sleep(3)
            await first_reply.delete()
    @commands.command()
    async def chaeyoung(self,message):
        if message.author.id == 467172810540843035:
            r = requests.api.get(f'https://meme-api.herokuapp.com/gimme/chaeyoung/3').json()
            z = []
            for x in r['memes']:
                z.append(f'{x["url"]}')
            embed = discord.Embed(title=discord.Embed.Empty,description="----------------------------------\n"
                                                                        "----------------------------------\n"
                                                                        "----------------------------------\n"
                                                                        "----------------------------------\n"
                                                                        "----------------------------------\n"
                                                                        "----------------------------------\n")
            embed.set_image(url=z[0])
            embed.set_thumbnail(url=z[1])
            await message.send(embed=embed)
        else:
            raise commands.MissingPermissions(["Chaeyoung's husband"])

    @commands.command()
    async def gif(self, message, *,search_query):
        first_msg = await message.send('**Retriving data**')
        apikey = "BYONSOOTKGT4"
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_query, apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty, description=discord.Embed.Empty, color=discord.colour.Color.blue())
            embed.set_author(name="HUSK GIF",
                             icon_url='https://cdn6.aptoide.com/imgs/e/8/7/e87cd92ea75d17a681b1eef6b2b83670_icon.png')
            embed.set_image(url=gif['url'])
            embed.set_footer(text=f'size, about : {(gif["size"]/1000).__round__()}KB')
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`', delete_after=5)

def setup(bot):
    bot.add_cog(Maincommands(bot))
    print('maincommands.py loaded')