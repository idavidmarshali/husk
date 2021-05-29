import discord, json, webcolors, requests, random, time
from discord.ext import commands
from sdk import husk_sdk

t = time.strftime('%H:%M:%S', time.localtime())
config = husk_sdk.BotConfig("./bot.json")
config.Load()


class MainCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    # Command zone------------↴
    @commands.has_guild_permissions(move_members=True)
    @husk_sdk.vc_checker()
    @commands.command(name="moveall",
                      brief="Moves all the Members in guild voice channels to the authors voiceChannel!")
    async def moveall(self, ctx: commands.Context):
        toMove = [mem for voice in [voice.members for voice in ctx.guild.voice_channels
                                    if voice.members is not None] for mem in
                  voice]  ##gets a list of every member in a VC
        moved = []
        for member in toMove:
            if member != ctx.author and member not in ctx.author.voice.channel.members:
                await member.move_to(ctx.author.voice.channel)
                moved.append(member)
        embeddef = husk_sdk.DefaultEmbed('moveall', ctx)
        embed = discord.Embed(title=f"Moved `{len(moved)} Members` to `{ctx.author.voice.channel.name}`",
                              description="**__Moved Members__**:\n" +
                                          "\n".join([member.mention for member in moved]), color=discord.Color.random()) \
            .set_author(name=embeddef.header, url=embeddef.header_url) \
            .set_footer(text=embeddef.footer, icon_url=embeddef.footer_icon) if moved != [] else \
            discord.Embed(title=f"{embeddef.header}", description="**🚫 No one is in other VoiceChannels!**",
                          color=discord.Color.red())
        await ctx.reply(embed=embed, delete_after=None if moved != [] else 10)

    @commands.command(name="ping", brief="Gives you The Ping of the bot in milliseconds!")
    async def ping(self, message):
        await message.reply(f"**BOTs ping is :** `{int(self.bot.latency * 1000)}ms`")

    @commands.has_guild_permissions(manage_messages=True)
    @commands.command(aliases=['del', 'clear', 'delete', 'clearchat', 'cl'], name="chatclear",
                      brief=f"will delete the amount of messages given to it! can get member too, {config.prefix}cl limit MentionedMember")
    async def chatclear(self, ctx: commands.Context, arg=5, member: discord.Member = None):
        await ctx.message.delete()
        if not arg <= 100 and arg >= 1:
            raise husk_sdk.OverTheLimit("1 -> 100", arg)
        else:
            menu = husk_sdk.ClMenu(arg, member)
            await menu.start(ctx)

    @commands.has_guild_permissions(mute_members=True)
    @commands.command(name="muteall", brief="Mutes every member in the commands caller voiceChannel except "
                                                  "himself!")
    async def muteall(self, ctx: commands.Context):
        muted = []
        for member in ctx.author.voice.channel.members:
            if member != ctx.author:
                await member.edit(mute=True)
                muted.append(member)
        embeddef = husk_sdk.DefaultEmbed('muteall', ctx)
        embed = discord.Embed(title=f"Muted `{len(muted)} Members` in `{ctx.author.voice.channel.name}`",
                              description="**__Muted Members__**:\n" +
                                          "\n".join([member.mention for member in muted]), color=discord.Color.random()) \
            .set_author(name=embeddef.header, url=embeddef.header_url) \
            .set_footer(text=embeddef.footer, icon_url=embeddef.footer_icon) if muted != [] else \
            discord.Embed(title=f"{embeddef.header}", description="**🚫 No one is in your VoiceChannel Except You!**",
                          color=discord.Color.red())
        await ctx.reply(embed=embed, delete_after=None if muted != [] else 10)

    @commands.has_guild_permissions(mute_members=True)
    @commands.command(name="unmuteall", brief="Unmutes every muted person in the command callers voiceChannel!")
    async def unmuteall(self, ctx: commands.Context):
        unmuted = []
        for member in ctx.author.voice.channel.members:
            if member.voice.mute:
                await member.edit(mute=False)
                unmuted.append(member)
        embeddef = husk_sdk.DefaultEmbed('muteall', ctx)
        embed = discord.Embed(title=f"UnMuted `{len(unmuted)} Members` in `{ctx.author.voice.channel.name}`",
                              description="**__UnMuted Members__**:\n" +
                                          "\n".join([member.mention for member in unmuted]),
                              color=discord.Color.random()) \
            .set_author(name=embeddef.header, url=embeddef.header_url) \
            .set_footer(text=embeddef.footer, icon_url=embeddef.footer_icon) if unmuted != [] else \
            discord.Embed(title=f"{embeddef.header}", description="**🚫 No one is Muted in your VoiceChannel!**",
                          color=discord.Color.red())
        await ctx.reply(embed=embed, delete_after=None if unmuted != [] else 10)

    @commands.has_guild_permissions(mute_members=True)
    @commands.command(aliases=['user', 'info'], name="check", brief="Checks and gives you the specified Users"
                                                                          "Detail and server Specific detail!")
    async def check(self, ctx: commands.Context, user: discord.User):
        member: discord.Member = discord.utils.get(ctx.guild.members, id=user.id)
        try:
            color_web = webcolors.name_to_rgb(f'{user.default_avatar}')
            color = discord.Colour.from_rgb(color_web.red, color_web.green, color_web.blue)
        except ValueError:
            color = discord.Color.random()
        embeddf = husk_sdk.DefaultEmbed('Check', ctx=ctx)
        embed = discord.Embed(title=f"User's DisplayName: `{user.display_name}`",
                              description=f"**User's id** : `{user.id}`\n"
                                          f"**User's Discriminator** : `#{user.discriminator}`",
                              colour=color)
        embed.set_author(name=embeddf.header, url=embeddf.header_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_footer(text=embeddf.footer, icon_url=embeddf.footer_icon)
        embed.add_field(name="`Account Specific Detail`**:**",
                        value=f"""```Account Created in : {user.created_at.strftime('%Y-%m-%d')}
Animated Profile Avatar? : {'Yes' if user.avatar.is_animated() else 'No'}
is a Bot? : {'Yes' if user.bot else 'No'}
Default Avatar Color : {user.default_avatar}
Current Activity : {member.activity.name if member.activity is not None else 'Nothing'}
is on mobile? : {'Yes' if member.is_on_mobile() else 'No'}
Status : {'Do not Disturb' if member.status == 'dnd' else member.status}```""")
        embed.add_field(name=f"`Server Specific Detail`**:**",
                        value=f"""```current Server : {ctx.guild.name}
NickName : {'None' if member.nick is None else member.nick}
joined the server at : {member.joined_at.strftime("%Y-%m-%d")}
Top Role : {member.top_role.name}
Is Boosting the server? : {'Yes' if member.premium_since is not None else 'No'}
Server Roles : {"-".join([role.name for role in member.roles if role.name != "@everyone"])}
is Server Owner : {'Yes' if member == ctx.guild.owner else 'No'}
                        ```""",
                        inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['bug'], name="report", brief="Report any bugs of the bot to the bot operator!")
    async def report(self, ctx: commands.Context, *, bug):
        op: discord.User = self.bot.get_user(config.operator_id)
        embed = discord.Embed(title="BUG REPORT", description=f"Reported by {ctx.author.mention} at "
                                                              f"`{ctx.message.created_at.strftime('%m-%d  %H : %M : %S')}`. "
                                                              f"\n **BUG** : ```{bug}```", color=discord.Color.random())
        await op.send(embed=embed)
        await ctx.reply(f"**Thank You!** `Bug was reported successfully!`")

    # Not changed in the update
    @commands.command(aliases=['gimme'], name="meme",
                      brief="Gives you a meme from r/meme or r/dankmeme or r/me_irl")
    async def meme(self, ctx: commands.Context):
        wait_msg = await ctx.send(f'**Retrieving Data** ')
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
                await ctx.message.delete()
            else:
                await wait_msg.edit(content=f'**Failed, Respond Code : `{respond.status_code}`**', delete_after=10)
                await ctx.message.delete()
        except requests.exceptions.ConnectionError:
            await wait_msg.edit(content=f'**Connection Error, Try Again**', delete_after=10)
            await ctx.message.delete()

    # Not changed in the update
    @commands.command(name="subreddit", brief="Gives you a Random post from the givien subreddit name")
    async def subreddit(self, message, subreddit_name):
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

        r = requests.api.get(f'https://meme-api.herokuapp.com/gimme/{subreddit_name}')
        if r.status_code == 200:
            data = r.json()
            if data['nsfw']:
                if message.channel.is_nsfw():
                    await message.send(embed=embed_msg(data))
                else:
                    x = await message.send(f'**NSFW** | `🔞` `{message.channel} is not an NSFW channel!`')
                    time.sleep(3)
                    await x.delete()
                    await message.message.delete()
            else:
                await message.send(embed=embed_msg(data))
        else:
            await message.send(f'**REDDIT ERROR** | `🚫` `{r.json()}`', delete_after=5)
            await message.message.delete()

    @commands.command(name="hex", brief="Encodes or Decodes Text into Hexodecimal Values!")
    @commands.guild_only()
    async def hex(self, ctx: commands.Context):
        menu = husk_sdk.HexMenu(bot=self.bot)
        await menu.start(ctx)

    # only api config change in the Update
    @commands.command(name="gif", brief="gives you a gif from the search query!", category="Fun")
    async def gif(self, message, *, search_query):
        first_msg = await message.send('**Retriving data**')
        apikey = config.gif_apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_query, apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty, description=discord.Embed.Empty,
                                  color=discord.colour.Color.blue())
            embed.set_author(name="HUSK GIF",
                             icon_url='https://cdn6.aptoide.com/imgs/e/8/7/e87cd92ea75d17a681b1eef6b2b83670_icon.png')
            embed.set_image(url=gif['url'])
            embed.set_footer(text=f'size, about : {(gif["size"] / 1000).__round__()}KB')
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @commands.command(aliase=["info"], name="about", brief="About this bot!", description="Information about this bot!")
    async def about(self, ctx):
        me = self.bot.get_user(393073095956496384)
        embeddf = husk_sdk.DefaultEmbed("Info", ctx)
        embed = discord.Embed(title=f"`{config.name}` **Information**", description=f"`{config.name}`**is a bot Created"
                                                                                    f" by {me.mention} mainly for "
                                                                                    f"personal uses. the bot has been "
                                                                                    f"written in [Python]("
                                                                                    f"https://www.python.org) using ["
                                                                                    f"discord.py]("
                                                                                    f"https://github.com/Rapptz"
                                                                                    f"/discord.py) library. \nthe "
                                                                                    f"bots Answering AI is based on "
                                                                                    f"the [CleverBot AI]("
                                                                                    f"https://www.cleverbot.com/) "
                                                                                    f"interface, and the bots reddit "
                                                                                    f"commands are based on [Reddits "
                                                                                    f"Api](https://www.reddit.com"
                                                                                    f"/) and the gif api is based on "
                                                                                    f"[tenors api](https://www.tenor.com)"
                                                                                    f"\nYou can see more about the "
                                                                                    f"bot at its github repo as its "
                                                                                    f"an opensource discord-bot: ["
                                                                                    f"Click to View](https://github.com/idavidmarshali/husk)**"
                                                                                    f"\n**Current Bot Version: {config.version}** ",
                              colour=discord.Color.random())
        embed.set_thumbnail(url=me.avatar_url)
        embed.set_footer(text=embeddf.footer, icon_url=embeddf.footer_icon)
        await ctx.send(embed=embed)
    @commands.command()
    async def update(self, ctx):
        embeddf = husk_sdk.DefaultEmbed("Update",ctx)
        embed = discord.Embed(title=embeddf.header, description=f"`**You can see the new updates in "
                                                                                    f"the bots repo : "
                                                                                    f"[Click Here]"
                                                                            f"(https://github.com/idavidmarshali/husk)**",
                              colour=discord.Color.random())
        embed.set_footer(text=embeddf.footer, icon_url=embeddf.footer_icon)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(MainCommands(bot))
    print('maincommands.py loaded')
