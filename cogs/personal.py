import discord
from discord.ext import commands
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

def setup(bot):
    bot.add_cog(PersonalCommands(bot))
    print('personal.py loaded')