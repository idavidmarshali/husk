import discord
from discord.ext import commands
import time
import json


## logger stat checker
def logger_stat_checker(server_id):
    try:
        with open('./servers.json', 'r') as file:
            data = json.load(file)
        if f'{server_id}' in data['servers']:
            if data['servers'][f'{server_id}']["log_stat"] == 'off':
                return False, 'false'
            elif data['servers'][f'{server_id}']["log_stat"] == 'on':
                return True, data['servers'][f'{server_id}']['log_channel']
        else:
            return False, 'false'
    except json.decoder.JSONDecodeError:
        print('json decoder error happened as always')


##                    ##
t = time.strftime('%H:%M:%S', time.localtime())
prefix = '!!'


class Logger(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # EVENT ZONE ----------↴
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member.id != 279542983907344384 and member.id != 393073095956496384:
            log_stat = logger_stat_checker(member.guild.id)
            if log_stat[0]:
                channel = self.bot.get_channel(log_stat[1])
                global t
                if before.channel == None:
                    await channel.send(
                        f"**VC** | **USER : {member.mention}** Joined from No where to`{after.channel.name}` at"
                        f" `{t}`")
                elif after.channel == None:
                    await channel.send(
                        f"**VC** | **USER : {member.mention}** Disconnected From `{before.channel.name}` at `{t}`")
                elif before.channel.id != after.channel.id:
                    await channel.send(
                        f"**VC** | **USER : {member.mention}** Went from `{before.channel.name}` to `{after.channel.name}` at `{t}`")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 555067760703569960:
            sv_roles = {
                '╔--🅢🅔🅡🅥🅔🅡 🅟🅔🅡🅜🅢--/': 710519764346470510,
                '╠-𝐃𝐒 𝐌𝐞𝐦𝐛𝐞𝐫𝐬': 710511844594286592,
                '╠-🅖🅔🅝🅓🅔🅡 🅟🅔🅡🅜🅢--/': 710526275445587998,
                '╠-🅐🅖🅔 🅟🅔🅡🅜🅢---/': 710552556254003270,
                '╠-🅖🅐🅜🅔 🅟🅔🅡🅜🅢--/': 710526428327968870,
                '╚-----------------------': 710530886470336673,
            }
            for role in sv_roles:
                r = member.guild.get_role(sv_roles[role])
                await member.add_roles(r)
        with open('./servers.json', 'r') as file:
            data = json.load(file)
        chan = self.bot.get_channel(data['servers'][f'{member.guild.id}']['welcome_chan'])
        if member.guild.id == 555067760703569960:
            title = '𝑺𝒉𝒂𝒅𝒐𝒘 𝑶𝒇 𝑾𝒂𝒓𝒓𝒊𝒐𝒓𝒔'
        else:
            title = member.guild.name
        embed = discord.Embed(title=title, description="", color=0xc70000)
        embed.add_field(name="----------↴", value=f"{member.mention} Welcome to the server", inline=False)
        embed.set_footer(text=f'User Joined in {t}')
        embed.set_thumbnail(url=member.avatar_url)
        await chan.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        log_stat = logger_stat_checker(member.guild.id)
        if log_stat[0] == True:
            with open('./servers.json', 'r') as file:
                data = json.load(file)
            chan = self.bot.get_channel(id=data['servers'][f'{member.guild.id}']['welcome_chan'])
            await chan.send(f"**USER : {member.mention}** Left from the Server at `{t}`")

    @commands.Cog.listener()
    async def on_member_ban(self, guild, member):
        log_stat = logger_stat_checker(guild.id)
        if log_stat[0]:
            channel = self.bot.get_channel(id=log_stat[1])
            await channel.send(f"**MOD** | **USER : {member.name}** has been banned from `{guild}` at `{t}`")

    @commands.Cog.listener()
    async def on_member_unban(self, guild, member):
        log_stat = logger_stat_checker(guild.id)
        if log_stat[0] == True:
            channel = self.bot.get_channel(id=log_stat[1])
            await channel.send(f"**MOD** | **USER : {member.name}** has been banned from `{guild}` at `{t}`")

    @commands.Cog.listener()
    async def on_member_kick(self, guild, member):
        log_stat = logger_stat_checker(guild.id)
        if log_stat[0] == True:
            channel = self.bot.get_channel(id=log_stat[1])
            await channel.send(f"**MOD** | **USER : {member.mention}** has been kicked from `{guild}` at `{t}`")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Me  -  Alireza
        try:
            if message.author.id != 393073095956496384 and message.author.id != 279542983907344384:
                log_stat = logger_stat_checker(message.guild.id)
                if log_stat[0] == True:
                    if not message.author.bot:
                        channel = self.bot.get_channel(id=log_stat[1])
                        await channel.send(
                            f"**LOGG** | **USER : {message.author.mention}** said : `{message.content}`  "
                            f"in `{message.channel}`")
        except AttributeError:
            pass

    # Command ZONE ----------↴
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def logger(self, message, arg=None):
        try:
            if arg == None:
                embed = discord.Embed(title=f"**Logger Stat** : {logger_stat_checker(message.guild.id)[0]}",
                                      description="▰▱▰▱▰▱▰▱",
                                      color=0x0040ff)
                embed.set_author(name="𝗛𝘂𝘀𝗸 𝗹𝗼𝗴𝗴𝗲𝗿 𝘀𝘁𝗮𝘁")
                embed.set_thumbnail(url='https://cdn.iconscout.com/icon/free/png-512/log-file-1-504262.png')
                embed.set_footer(text=f'{prefix}logger - exec at {t} - by {message.author}', )
                embed.add_field(name="The bot is logging:",
                                value="1- *Members Voice Stat* \n2- *Members Chat in sv*\n3- *MOD actions*",
                                inline=False)
                await message.send(embed=embed)
            elif arg == 'off':
                with open('./servers.json', 'r') as file:
                    data = json.load(file)

                if logger_stat_checker(message.guild.id)[0]:
                    data['servers'][f'{message.guild.id}']["log_stat"] = 'off'
                    with open('./servers.json', 'w') as file:
                        json.dump(data, file)
                        await message.send(f'**Attention** : `Logger is now offline`')
                elif not logger_stat_checker(message.guild.id)[0]:
                    await message.send(f'`🔹 Logger is already offline` **use `{prefix}logger on`** to turn it online')
            elif arg == 'on':
                with open('./servers.json', 'r') as file:
                    data = json.load(file)
                if logger_stat_checker(message.guild.id)[0]:
                    await message.send(f'`🔹 Logger is already Online` **use `{prefix}logger on`** to turn it Offline')
                elif not logger_stat_checker(message.guild.id)[0]:
                    data['servers'][f'{message.guild.id}']["log_stat"] = 'on'
                    with open('./servers.json', 'w') as file:
                        json.dump(data, file)
                        await message.send(f'**Attention** : `Logger is now online`')
        except json.decoder.JSONDecodeError:
            print(f'error in {prefix}logger')


def setup(bot):
    bot.add_cog(Logger(bot))
    print('logger.py loaded')