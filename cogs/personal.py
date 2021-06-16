import discord, os
from discord.ext import commands
from discord_components import Button, ButtonStyle, Interaction, Select, Option
import requests

class PersonalCommands(commands.Cog):
        def __init__(self, bot):
            self.bot: commands.Bot = bot

        @commands.command(hidden=True)
        async def chaeyoung(self, message):

            if message.author.id == 467172810540843035:
                r = requests.api.get(f'https://meme-api.herokuapp.com/gimme/chaeyoung/3').json()
                z = []
                for x in r['memes']:
                    z.append(f'{x["url"]}')
                embed = discord.Embed(title=discord.Embed.Empty, description="-")
                embed.set_image(url=z[0])
                embed.set_thumbnail(url=z[1])
                await message.send(embed=embed)
            else:
                raise commands.MissingPermissions(["Chaeyoung's husband"])
        @commands.command()
        async def save_all_emojis(self, ctx:commands.Context, limit=None, PATH = "G:\C-G\DiscordEmojis"):
            saved = []
            async for message in ctx.channel.history(limit=8):
                print(message.content)
                emojies = [reaction.emoji for reaction in message.reactions if reaction.custom_emoji]
                for emoji in emojies:
                    byte = await emoji.url.read()
                    url = str(emoji.url)
                    with open(PATH+f"\\{emoji.name}." + url.split("?")[0][-3:len(url.split("?")[0])], "wb") as file:
                        file.write(byte)
                    saved.append(emoji.name)
            embed = discord.Embed(title="DONE", description=f"```css\n[DONE]```", colour=discord.Color.red())
            print(f"List of saved Emojis :\n{''.join([f'-{name}-' for name in saved])}")
            await ctx.reply(embed=embed)

        @commands.command()
        async def update_emojis(self, ctx: commands.Context, PATH = "G:\C-G\DiscordEmojis"):
            added = []
            count = 0
            for file_name in os.listdir(PATH)[48:]:
                with open(PATH + f"\\{file_name}", "rb") as img:
                    await ctx.guild.create_custom_emoji(name=file_name.split(".")[0], image=img.read()) if os.stat(path=PATH + f"\\{file_name}").st_size < 256000 else None
                    added.append(file_name.split(".")[0])
                print(f"Done {count}")
                count+=1
            embed = discord.Embed(title="DONE",
                                  description=f"**List of saved Emojis :**\n```{''.join([f'-{name}-' for name in added])}```",
                                  colour=discord.Color.red())

            await ctx.reply(embed=embed)



def setup(bot):
    bot.add_cog(PersonalCommands(bot))
    print('personal.py loaded')