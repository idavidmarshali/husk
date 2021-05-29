import discord, json, requests, random, webcolors
from discord.ext import commands
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash import cog_ext, SlashContext
from sdk import husk_sdk

config = husk_sdk.BotConfig("./bot.json")
config.Load()

guild_ids = config.slashguilds


class SlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @cog_ext.cog_slash(name="gif", description="gives you a gif from the options!", options=[
        create_option(name="category", description="Your predefined gif options", option_type=3, required=True,
                      choices=[create_choice(value=x, name=x) for x in husk_sdk.getgifs()])],
                       guild_ids=guild_ids)
    async def s_gif(self, ctx: SlashContext, category: str):
        first_msg = await ctx.send('**Retriving data**')
        apikey = config.gif_apikey
        lmt = 50
        try:
            r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (category, apikey, lmt))
        except requests.exceptions.ConnectionError:
            return await ctx.send(f'**ERROR** | `🛑` `Something wet wrong, try again.`',
                                  delete_after=5)
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty, description=discord.Embed.Empty,
                                  color=discord.colour.Color.blue())
            embed.set_author(name="HUSK CAT GIFs",
                             icon_url='https://cdn6.aptoide.com/imgs/e/8/7/e87cd92ea75d17a681b1eef6b2b83670_icon.png')
            embed.set_image(url=gif['url'])
            embed.set_footer(text=f'size, about : {(gif["size"] / 1000).__round__()}KB')
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @cog_ext.cog_slash(guild_ids=guild_ids, name="clear",
                       description="Deletes the amount of messages givin to it based on the user, default is global purge!",
                       options=[create_option(name="amount", description="Amount of messages to delete!", option_type=4,
                                              required=True),
                                create_option(name="user", description="specific user to check", option_type=6,
                                              required=False)])
    async def s_clear(self, ctx: SlashContext, amount: int, user: discord.Member = None):
        if not amount <= 100 and amount >= 1:
            raise husk_sdk.OverTheLimit("1 -> 100", amount)
        else:
            check = lambda message: (message.author == user) if user is not None else True
            await ctx.channel.purge(limit=amount, check=check)
            embed = discord.Embed(title=f"**DONE :-)**",
                                  description=f"```dif\nThe Amount of {amount} messages have been purged from" \
                                              f" {ctx.channel.name}```" \
                                      if user is None else f"```dif\nThe Amount of {amount} messages from {user.display_name}" \
                                                           f" have been purged from {ctx.channel.name}```")
            embed.set_footer(text=f"Used by 🔹{ctx.author.display_name}🔹"
                             , icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="moveall", description="Moves all the members in a server, to authors VoiceChannel!",
                       guild_ids=guild_ids)
    async def s_moveall(self, ctx: SlashContext):
        toMove = [mem for voice in [voice.members for voice in ctx.guild.voice_channels
                                    if voice.members is not None] for mem in
                  voice]  ##gets a list of every member in a VC
        moved = []
        for member in toMove:
            if member != ctx.author and member not in ctx.author.voice.channel.members:
                await member.move_to(ctx.author.voice.channel)
                moved.append(member)
        embed = discord.Embed(title=f"Moved `{len(moved)} Members` to `{ctx.author.voice.channel.name}`",
                              description="**__Moved Members__**:\n" +
                                          "\n".join([member.mention for member in moved]), color=discord.Color.random()) \
            .set_footer(text=f"Used by 🔹{ctx.author.display_name}🔹",
                        icon_url=ctx.author.avatar.url) if moved != [] else \
            discord.Embed(title=f"**Moveall command**", description="**🚫 No one is in other VoiceChannels!**",
                          color=discord.Color.red())
        await ctx.send(embed=embed, delete_after=None if moved != [] else 10)

    @cog_ext.cog_slash(name="muteall", description="Mutes all the members in authors VC!",
                       guild_ids=guild_ids)
    async def s_muteall(self, ctx: commands.Context):
        muted = []
        for member in ctx.author.voice.channel.members:
            if member != ctx.author:
                await member.edit(mute=True)
                muted.append(member)
        embed = discord.Embed(title=f"Muted `{len(muted)} Members` in `{ctx.author.voice.channel.name}`",
                              description="**__Muted Members__**:\n" +
                                          "\n".join([member.mention for member in muted]), color=discord.Color.random()) \
            .set_footer(text=f"Used by 🔹{ctx.author.display_name}🔹",
                        icon_url=ctx.author.avatar.url) if muted != [] else \
            discord.Embed(title=f"**Muteall command**", description="**🚫 No one is in this VoiceChannel except you!**",
                          color=discord.Color.red())
        await ctx.send(embed=embed, delete_after=None if muted != [] else 10)

    @cog_ext.cog_slash(name="unmuteall", description="Unmutes all the members in authors VC!", guild_ids=guild_ids)
    async def s_unmuteall(self, ctx: commands.Context):
        unmuted = []
        for member in ctx.author.voice.channel.members:
            if member.voice.mute:
                if member != ctx.author:
                    await member.edit(mute=False)
                    unmuted.append(member)
        embed = discord.Embed(title=f"UnMuted `{len(unmuted)} Members` in `{ctx.author.voice.channel.name}`",
                              description="**__UnMuted Members__**:\n" +
                                          "\n".join([member.mention for member in unmuted]),
                              color=discord.Color.random()) \
            .set_footer(text=f"Used by 🔹{ctx.author.display_name}🔹",
                        icon_url=ctx.author.avatar.url) if unmuted != [] else \
            discord.Embed(title=f"**UnMuteall command**",
                          description="**🚫 No one is in this VoiceChannel except you!**",
                          color=discord.Color.red())
        await ctx.send(embed=embed, delete_after=None if unmuted != [] else 10)

    @cog_ext.cog_slash(name="check", description="Gives you info about an specific member anonymously",
                        options=[create_option(name="user", description="specific user to check", option_type=6,
                                              required=True)], guild_ids=guild_ids)
    async def s_check(self, ctx: SlashContext, user: discord.User):
        member: discord.Member = discord.utils.get(ctx.guild.members, id=user.id)
        try:
            color_web = webcolors.name_to_rgb(f'{user.default_avatar}')
            color = discord.Colour.from_rgb(color_web.red, color_web.green, color_web.blue)
        except ValueError:
            color = discord.Color.random()
        embed = discord.Embed(title=f"User's DisplayName: `{user.display_name}`",
                              description=f"**User's id** : `{user.id}`\n"
                                          f"**User's Discriminator** : `#{user.discriminator}`",
                              colour=color)

        embed.set_thumbnail(url=user.avatar.url)
        embed.set_footer(text=f"Used by 🔹{ctx.author.display_name}🔹",
                         icon_url=ctx.author.avatar.url)
        embed.add_field(name="`Account Specific Detail`**:**",
                        value=f"""```Account Created in : {user.created_at.strftime('%Y-%m-%d')}
Animated Profile Avatar? : {'Yes' if user.avatar.is_animated() else 'No'}
is a Bot? : {'Yes' if user.bot else 'No'}
Default Avatar Color : {user.colour}
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
        await ctx.send(embed=embed, hidden=True)
    @cog_ext.cog_slash(name="hentai", description="Gives you some good stuff from r/hentai", options=[
        create_option(name="hidden", description="Only you can see the result if `YES`", required=False, option_type=4, choices=[
            create_choice(name="YES, just for me", value=1), create_choice(name="NO, lets enjoy it together", value=0)])], guild_ids=guild_ids)
    async def s_hentai(self, ctx: SlashContext, hidden: int = 0):
        hidden = bool(hidden)
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

        r = requests.api.get(f'https://meme-api.herokuapp.com/gimme/hentai')
        if r.status_code == 200:
            data = r.json()
            if data['nsfw']:
                if ctx.channel.is_nsfw():
                    await ctx.send(embed=embed_msg(data), hidden=hidden)
                else:
                    await ctx.send(f'**NSFW** | `🔞` `{ctx.channel.name} is not an NSFW channel!`', hidden=hidden)
            else:
                await ctx.send(embed=embed_msg(data), hidden=hidden)
        else:
            await ctx.send(f'**REDDIT ERROR** | `🚫` `{r.json()}`')
def setup(bot):
    bot.add_cog(SlashCommands(bot))
    print('slashcommands.py loaded')
