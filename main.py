import discord
from discord.ext import commands, tasks
import requests
from itertools import cycle
import json
import os
import time
import discord.utils
import discord
import aiohttp
import async_cleverbot as ac
from cogs.maincommands import check
import traceback

intents = discord.Intents().all()
prefix='!!'
status = cycle([f'{prefix}help','Baby Shark do do..','Boty Shark do do..','ха-ха, я заставил тебя перевести на русский'])
bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True)
bot.remove_command('help')

moods = {
    "joy": ac.Emotion.joy,
    "anger": ac.Emotion.anger,
    "angry": ac.Emotion.angry,
    "fear": ac.Emotion.fear,
    "sad": ac.Emotion.sad,
    "sadness": ac.Emotion.sadness,
    "happy": ac.Emotion.happy,
    "neutral": ac.Emotion.neutral,
    "normal": ac.Emotion.normal,
    "scared": ac.Emotion.scared
}
mood = moods["normal"]
@bot.event
async def on_ready():
    status_update.start()
    print('The bot has logged in as {0.user}\n-------------------↴'.format(bot))

# EVENT ZONE ----------↴
@bot.event
async def on_message(message):
    if message.content.lower().startswith("husk") and len(message.content[0:4]) > 3:
        cb = ac.Cleverbot("s<&wv.@K@k/Yne(Bj<:E")
        async with message.channel.typing():
            respond = await cb.ask(message.content[4:], emotion=mood)
            await message.channel.send(f"**HUSK** : `{respond.text}`")
            if respond.text.endswith("?"):
                res = await bot.wait_for("message", check=check(message.author), timeout=10)
                respond = await cb.ask(res.content, emotion=mood)
                await message.channel.send(f"**HUSK** : `{respond.text}`")
            await cb.close()
    await bot.process_commands(message)


#######################
# main error handler #
#####################

@bot.event
async def on_command_error(message :discord.message, error):
    error = getattr(error,'original',error)
    if isinstance(error, commands.CommandNotFound):
        await message.send(f"**ERROR** | `🚫` `Command Not Found, Use {prefix}help to see the bots commands`",
                           delete_after=3)
        await message.message.delete()
    elif isinstance(error, commands.MissingPermissions):
        await message.send(f"**ERROR** | `🚫` `{error}`", delete_after=3)
        await message.message.delete()
    elif isinstance(error, commands.MissingRequiredArgument):
        await message.send(f"**ERROR** | `🚫` `{error}`", delete_after=3)
        await message.message.delete()
    elif isinstance(error, commands.UserNotFound):
        x = await message.send(f"**ERROR** | `🚫` `{error}`", delete_after=3)
        time.sleep(3)
        await x.delete()
        await message.message.delete()
    elif isinstance(error, commands.CommandInvokeError):
        await message.send(f'**ERROR** | `{error}`', delete_after=5)
    elif isinstance(error, TimeoutError):
        await message.send(f'**ERROR** | `{error}`', delete_after=5)
        await message.message.delete()
    else:
        print(error)








@commands.is_owner()
@bot.command()
async def set_mood(ctx, inpmood: str):
    global mood
    try:
        mood = moods[inpmood]
        await ctx.send(f"**Done!, mood set to `{inpmood}`**", delete_after=5)
    except:
        await ctx.send("**Wrong Mood Given**", delete_after=5)

# COMMAND ZONE ----------↴
@bot.command()
async def help(message, arg: str=None):
    print(arg)
    if arg is None:
        me: discord.User = bot.get_user(393073095956496384)
        member_emoji: discord.Emoji = bot.get_emoji(id=798482024414576720)
        admin_emoji: discord.Emoji=bot.get_emoji(798482007599874080)
        gif_emoji:discord.Emoji=bot.get_emoji(798481994219520020)
        line_emoji = bot.get_emoji(798508521519317032)
        embed = discord.Embed(title=discord.Embed.Empty,description=discord.Embed.Empty, color=0xfc8ba0)
        embed.add_field(name=f'**{admin_emoji}Moderator Commands:**',value=f'{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}'
                                                                           f'```{prefix}logger``````{prefix}moveall``````{prefix}muteall``````{prefix}unmuteall``````{prefix}clear [amount]``````{prefix}moverage [User]``````{prefix}ban [User]``````{prefix}kick [User]```',inline=True)
        embed.add_field(name=f'**{member_emoji}Member Commands :**', value=f'{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}'
                                                                           f'```{prefix}report [describe bug]``````{prefix}hex``````{prefix}meme or {prefix}gimme``````{prefix}subreddit [subreddits name]``````{prefix}check [user]``````{prefix}about```',inline=True)
        embed.add_field(name=f'**{gif_emoji}gif commands :**', value=f'{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}{line_emoji}'
                                                                     f'```{prefix}gif [Search Term]``````{prefix}dog``````{prefix}cat``````{prefix}kiss [user]``````{prefix}slap [user]``````{prefix}smile``````{prefix}spank [user]``````{prefix}lick [user]``````{prefix}cuddle [user]``````{prefix}sleep```')
        embed.add_field(name=f"**Pls Note that all of the commands are fully described at {prefix}help [commands name]**", value=f"for example : `{prefix}help logger`", inline=False)
        embed.set_author(name='HUSK HELP MENU')
        embed.set_footer(text=f'Created by {me}', icon_url=me.avatar_url)
        await message.send(embed=embed, delete_after=30)
    elif arg.lower() == 'logger':
        embed=discord.Embed(title='```Husk Logger Help Menu```', description=f'Husk\'s logging service is a great way '
                                                                             f'to logg what you user\'s are doing in '
                                                                             f'your server.\n Husk currently has `3` '
                                                                             f'logging commands.\n ```diff\n-1- '
                                                                             f'{prefix}logger on  \n+Creat\'s a '
                                                                             f'privet text channel [if its the first '
                                                                             f'time using this command!] that is only '
                                                                             f'accessible by the admins and Then '
                                                                             f'starts the logging in '
                                                                             f'there```\n```diff\n-2- !!logger '
                                                                             f'off\n+Stop\'s the logger from '
                                                                             f'logging.```\n```diff\n-3- !!logger '
                                                                             f'\n+Show\'s the loggers status [is it '
                                                                             f'on/off, what is the logger logging, '
                                                                             f'where is it logging]```'
                            , color=0x7c960b).set_footer(text='⚠ Will be automatically Deleted in 15seconds!!')
        await message.send(embed=embed, delete_after=25)
    elif arg.lower() == 'moveall':
        embed = discord.Embed(title='```Husk MoveAll Help Menu```',
                              description=f'**The `{prefix}Moveall` is a command for users who have `move members` '
                                          f'permission and when executed, it will `move` every member who is in a '
                                          f'`voice channel` in the server, to the person who called to commands '
                                          f'channel!!**', color=0x342423)
        await message.send(embed=embed, delete_after=25)
    elif arg.lower() == 'muteall' or arg.lower() == 'unmuteall':
        embed = discord.Embed(title=f'```Husk {arg} Help Menu```',
                              description=f'**The `{prefix}{arg}` is a command for users who have `Mute members` '
                                          f'permission and when executed, it will `Mute The Microphone` of every '
                                          f'member who is in `the user who called the commands` voice channel!!** ',
                              color=0x87e8d5)
        await message.send(embed=embed, delete_after=25)
    elif arg.lower() == 'clear':
        embed = discord.Embed(title=f'```Husk {arg} Help Menu```',
                              description=f'**The `{prefix}{arg}` is a command for users who have `Manage Messages` '
                                          f'permission and when executed, it will `delete the amount of messages '
                                          f'given` to it in the `TextChannel that it has been called`, `default value '
                                          f'is 5`, so if you call the command with no value given it will delete 5 '
                                          f'messages by default!!** '
                              , color=0xa360bf)
        await message.send(embed=embed, delete_after=25)
    await message.message.delete()







# LOOP ZONE ----------↴
@tasks.loop(minutes=5)
async def status_update():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name=status.__next__(), url='https://discord.gg/Pr6qtxSUve'))



# Etc. ZONE ----------↴
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

with open('bot.json','r') as file:
    data = json.load(file)
    token = data["bot"]["token"]
bot.run(token)
