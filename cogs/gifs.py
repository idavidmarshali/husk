import discord, json, requests, random
from discord.ext import commands
from sdk import husk_sdk

def user_check(user: discord.Member):
    if user is None:
        return "The air"
    if user is not None:
        return user.mention


class GifCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.apikey = bot.config.gif_apikey
    #cat - dog - kiss - spank - lick - smile - greet - sleep - slap - cuddle
    @commands.command()
    async def cat(self, message):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('cat', apikey, lmt))
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

    @commands.command()
    async def dog(self, message):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('Dog', apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty, description=discord.Embed.Empty,
                                  color=discord.colour.Color.blue())
            embed.set_author(name="HUSK DOG GIFs",
                             icon_url='https://cdn6.aptoide.com/imgs/e/8/7/e87cd92ea75d17a681b1eef6b2b83670_icon.png')
            embed.set_image(url=gif['url'])
            embed.set_footer(text=f'size, about : {(gif["size"] / 1000).__round__()}KB')
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @commands.command()
    async def kiss(self, message, user :discord.Member=None):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime_kiss', apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty, description=f"{message.author.name} **kissed** {user_check(user)}",
                                  color=0x0000)
            embed.set_image(url=gif['url'])
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @commands.command()
    async def slap(self, message, user: discord.Member = None):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime slap', apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty,
                                  description=f"{message.author.name} **slapped** {user_check(user)}",
                                  color=0x0000)
            embed.set_image(url=gif['url'])
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @commands.command()
    async def sleep(self, message):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime_kiss', apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty,
                                  description=f"{message.author.name} is going to sleep!",
                                  color=0x0000)
            embed.set_image(url=gif['url'])
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @commands.command()
    async def spank(self, message, user: discord.Member = None):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime spank', apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty,
                                  description=f"{message.author.name} **Spanked** {user_check(user)}",
                                  color=0x0000)
            embed.set_image(url=gif['url'])
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @commands.command()
    async def greet(self, message, user: discord.Member = None):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('aime greeting', apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty,
                                  description=f"{message.author.name} **greets** {user_check(user)}",
                                  color=0x0000)
            embed.set_image(url=gif['url'])
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @commands.command()
    async def smile(self, message, user: discord.Member = None):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime smile', apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty,
                                  description=f"{message.author.name} **smiled at** {user_check(user)}",
                                  color=0x0000)
            embed.set_image(url=gif['url'])
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @commands.command()
    async def lick(self, message, user: discord.Member = None):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime lick', apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty,
                                  description=f"{message.author.name} **licked** {user_check(user)}",
                                  color=0x0000)
            embed.set_image(url=gif['url'])
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)

    @commands.command()
    async def cuddle(self, message, user: discord.Member = None):
        first_msg = await message.send('**Retriving data**')
        apikey = self.apikey
        lmt = 50
        r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s" % ('anime cuddle', apikey, lmt))
        if r.status_code == 200:
            trending_gifs = json.loads(r.content)
            data = trending_gifs['results'][random.randint(0, trending_gifs['results'].__len__())]
            gif = None
            for nm in data['media']:
                if nm['gif']:
                    gif = nm['gif']
            embed = discord.Embed(title=discord.Embed.Empty,
                                  description=f"{message.author.name} **Cuddled** {user_check(user)}",
                                  color=0x0000)
            embed.set_image(url=gif['url'])
            await first_msg.edit(content=None, embed=embed)
        else:
            await first_msg.edit(
                content=f'**ERROR** | `🛑` `Something wet wrong, try again. Respond-Code :{r.status_code}`',
                delete_after=5)
def setup(bot):
    bot.add_cog(GifCommands(bot))