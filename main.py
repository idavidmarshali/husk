from discord.ext import commands, tasks
from itertools import cycle
import discord.utils, discord, os
from sdk import husk_sdk
import async_cleverbot as ac
from discord_slash import SlashCommand
from discord_components import DiscordComponents, Button
from discord_slash.utils.manage_commands import create_choice,create_option
from discord_slash.utils import manage_commands

config = husk_sdk.BotConfig("bot.json")
config.Load()
intents = discord.Intents().all()
prefix = config.prefix
status = cycle([f'{prefix}help', f'Version 2.0 Is Up', f'{prefix}Update to see it!',
                'Im UPDATED, Yaaaay!', 'slash commands are here!!'])
bot = commands.Bot(command_prefix=prefix, intents=intents, case_insensitive=True,
                   help_command=husk_sdk.HelpCommand())
bot.__setattr__("config", config)
slash = SlashCommand(bot, sync_commands=True)
def getbot():
    return bot

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
    DiscordComponents(bot)
    print('The bot has logged in as {0.user}\n-------------------↴'.format(bot))


# EVENT ZONE ----------↴
@bot.event
async def on_message(message):
    if message.content.lower().startswith("husk") and len(message.content[0:4]) > 3:
        await husk_sdk.call_CeleverBot(message, bot, mood)
    await bot.process_commands(message)


#######################
# main error handler #
#####################

@bot.event
async def on_command_error(ctx: commands.Context, error):
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"**ERROR** | `🚫` `Command Not Found, Use {prefix}help to see the bots commands`",
                           delete_after=3)
        await ctx.message.delete()
    else:
        errorlist = [commands.MissingPermissions,
                     commands.MissingRequiredArgument,
                     commands.UserNotFound,
                     commands.CommandInvokeError,
                     TimeoutError,
                     husk_sdk.NotInVoice,
                     husk_sdk.OverTheLimit,
                     commands.NotOwner]
        for er in errorlist:
            if isinstance(error, er):
                await ctx.send(f"**ERROR** | `🚫` `{error}`", delete_after=3)
                await ctx.message.delete()
                return
    print("ERROR:" + str(error))


# COMMAND ZONE ----------↴
@commands.is_owner()
@bot.command(hidden=True)
async def set_mood(ctx, inpmood: str):
    global mood
    try:
        mood = moods[inpmood]
        await ctx.send(f"**Done!, mood set to `{inpmood}`**", delete_after=5)
    except:
        await ctx.send("**Wrong Mood Given**", delete_after=5)

# LOOP ZONE ----------↴
@tasks.loop(minutes=2)
async def status_update():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status.__next__(),
                                                        url='https://discord.gg/Pr6qtxSUve'))


# Etc. ZONE ----------↴
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run(config.token)
