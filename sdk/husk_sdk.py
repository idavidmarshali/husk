from discord.ext import commands, menus
import discord, json, binascii, asyncio, random
import async_cleverbot as ac
from discord_components import ButtonStyle, Button, Interaction
import asyncio


# ///////////////////////
# Function Section ///
# ////////////////////

def vc_checker():
    """
    checks if the message.author is in a voicechannel or not.
    if is in a vc returns TRUE
    else raises husk_exceptions.NotInVoice()
    :returns bool:
    """

    def predict(message):
        if message.author.voice is not None:
            return True
        raise NotInVoice("You need to join a voice channel in order to use this command!")

    return commands.check(predict)


def getgifs():
    """
    returs a list of available emojies for /gif command
    :return:
    """
    return "cat-dog-kiss-spank-lick-smile-greet-sleep-slap-cuddle".split("-")


async def call_CeleverBot(message, bot, mood) -> None:
    """
    Api Caller for CleverBot Api!
    :param message:
    :param bot:
    :param mood:
    :return None:
    """
    cb = ac.Cleverbot("s<&wv.@K@k/Yne(Bj<:E")
    async with message.channel.typing():
        respond = await cb.ask(message.content[4:], emotion=mood)
        await message.channel.send(f"**HUSK** : `{respond.text}`")
        if respond.text.endswith("?"):
            res = await bot.wait_for("message", check=lambda smessage: smessage.author == message.author, timeout=10)
            respond = await cb.ask(res.content, emotion=mood)
            await message.channel.send(f"**HUSK** : `{respond.text}`")
        await cb.close()


# //////////////////////////////
# Exception(ERROR) Section ///
# ////////////////////////////
class NotInVoice(commands.BadArgument):
    """
    Error Raised in VC-Based Commands when ctx.author is not in a VC
    """

    def __init__(self, arg="You're not in any voiceChannels!"):
        self.arg = arg
        super().__init__(self.arg)


class OverTheLimit(commands.BadArgument):
    """
    Error for {prefix}Clear, too lazy stuff :/
    """

    def __init__(self, limit, arg):
        self.arg = arg
        self.limit = limit
        super().__init__("the limit is {0} you entered {1}".format(self.limit, self.arg))


# ////////////////////////////
# Object(Class) Section ///
# //////////////////////////
class MemoryGame():
    """
    BETA - DO NOT USE THIS YET
    """
    @classmethod
    def randomComponentGenrator(self, add=1, before=[]):
        for i in range(0, add):
            row = random.randint(0, 4)
            index = random.randint(0, 4)
            if before[row][index].style != ButtonStyle.red and before[row][index].style != ButtonStyle.green:
                before[row][index] = Button(emoji="🟥", style=ButtonStyle.red)
            else:
                row = random.randint(0, 4)
                index = random.randint(0, 4)
                before[row][index] = Button(emoji="🟥", style=ButtonStyle.red)
    @classmethod
    def defaultComponents(self):
        last_row = [Button(emoji="🟦", style=ButtonStyle.blue) for _ in range(3)]
        last_row.append(Button(label="Submit", style=ButtonStyle.green))
        last_row.append(Button(label="Exit", style=ButtonStyle.red))
        return [
            [Button(emoji="🟦", style=ButtonStyle.blue) for _ in range(5)],
            [Button(emoji="🟦", style=ButtonStyle.blue) for _ in range(5)],
            [Button(emoji="🟦", style=ButtonStyle.blue) for _ in range(5)],
            [Button(emoji="🟦", style=ButtonStyle.blue) for _ in range(5)],
            last_row
        ]
    @classmethod
    def getRedButton(cls, componentList: list):
        all_buttons = []
        for actionRow in componentList:
            for button in actionRow:
                all_buttons.append((componentList.index(actionRow), actionRow.index(button)))
        return all_buttons



class HelpCommand(commands.HelpCommand):
    """
    a custom Help command based on the default d.py HelpCommand for automated command adding
    """

    class HelpMenu(menus.Menu):
        """
        Basic Embed Menu for the help command
        """

        def __init__(self, command_list, helpObject):
            super().__init__(delete_message_after=True)
            self.commandList: list = command_list
            self.helpObject: commands.HelpCommand = helpObject
            self.pagelimit = 3  # limit to amount of commands in one menu page

        def formats(self):
            dict = {1: []}
            page = 1
            for command in self.commandList:
                if self.commandList.index(command) <= self.pagelimit * page:
                    dict[page].append(command) if not command.hidden else None
                else:
                    page += 1
                    dict[page] = [command]
            return dict

        async def send_initial_message(self, ctx, channel):
            self.embed = discord.Embed(title="__**HELP COMMAND**__", colour=discord.Color.random())
            self.dict = self.formats()
            self.pages = len(self.dict.keys())
            self.currentpage = 1
            [self.embed.add_field(inline=False, name=f"`{command.name}`",
                                  value=f"```css\n[{self.helpObject.clean_prefix}{command.name} {command.signature}]\ndescription: {command.brief}```\n")
             for command in self.dict[self.currentpage]]
            embeddf = DefaultEmbed("Help", self.ctx)
            self.embed.set_footer(text=embeddf.footer, icon_url=embeddf.footer_icon)
            self.message = await ctx.send(embed=self.embed, components=[
                [Button(label="Previous", style=ButtonStyle.blue), Button(label="Next", style=ButtonStyle.blue),
                 Button(label="Exit", style=ButtonStyle.gray)]])
            while True:
                respond = await self.bot.wait_for("button_click", check=lambda inter: inter.user == self.ctx.author,
                                                  timeout=20)
                await respond.respond(type=6)
                if respond.component.label == "Previous":
                    if self.currentpage >= 2:
                        self.currentpage -= 1
                        self.embed.clear_fields()
                        [self.embed.add_field(inline=False, name=f"`{command.name}`",
                                              value=f"```css\n[{self.helpObject.clean_prefix}{command.name} {command.signature}]\ndescription: {command.brief}```\n")
                         for command in self.dict[self.currentpage]]
                        await self.message.edit(embed=self.embed)
                    await respond.respond(type=6)
                elif respond.component.label == "Next":
                    if self.currentpage <= self.pages:
                        self.currentpage += 1
                        self.embed.clear_fields()
                        [self.embed.add_field(inline=False, name=f"`{command.name}`",
                                              value=f"```css\n[{self.helpObject.clean_prefix}{command.name} {command.signature}]\ndescription: {command.brief}```\n")
                         for command in self.dict[self.currentpage]]
                        await self.message.edit(embed=self.embed)
                elif respond.component.label == "Exit":
                    await self.message.edit(embed=DefaultEmbed.close(), components=[], delete_after=10)
                    await self.ctx.message.delete()

                    break
            return None

    async def send_bot_help(self, mapping):
        commanndsl = [command for commands in [commandlist for cog, commandlist in mapping.items() if
                                               getattr(cog, 'qualified_name', 'None') != "GifCommands"] for command in
                      commands]
        commanndsl.sort(key=lambda command: command.name)
        menu = self.HelpMenu(commanndsl, self)
        await menu.start(ctx=self.context)


class ClMenu(menus.Menu):
    """
    The Default Clear Menu for {Prefix}Clear!
    """

    def __init__(self, limit, member):
        super().__init__(timeout=20)
        self.target: discord.Member = member
        self.limit: int = limit

    async def send_initial_message(self, ctx, channel):
        embeddf = DefaultEmbed("Clear", ctx)
        embed = discord.Embed(colour=discord.Color.red(), title="**Clear Command Approval**",
                              description=f"```css\nAre You sure you want to delete"
                                          f" [{self.limit}] Messages From "
                                          f"[{self.target.display_name}] in "
                                          f"[{ctx.channel.name}] ?```" if self.target is not None else
                              f"```css\nAre You sure you want to delete "
                              f"[{self.limit}] Messages in "
                              f"[{ctx.channel.name}] ?```")
        embed.set_footer(text=embeddf.footer, icon_url=embeddf.footer_icon)
        self.embed = embed
        self.message = await ctx.send(embed=embed, components=[
            [Button(label="Approve", style=ButtonStyle.green), Button(label="Reject", style=ButtonStyle.red)]])

        respond: Interaction = await self.bot.wait_for("button_click",
                                                       check=lambda inter: inter.user == self.ctx.author, timeout=20)
        await respond.respond(type=6)
        if respond.component.label == "Approve":
            def check(message: discord.Message):
                if self.target is not None:
                    return (self.target == message.author) and (self.message.id != message.id)
                else:
                    return self.message.id != message.id

            await self.ctx.channel.purge(limit=self.limit, check=check)
            self.embed.colour = discord.Color.green()
            self.embed.title = f"**DONE :-)**"
            self.embed.description = f"```dif\nThe Amount of {self.limit} messages have been purged from" \
                                     f" {self.ctx.channel.name}```" \
                if self.target is None else f"```dif\nThe Amount of {self.limit} messages from {self.target.display_name}" \
                                            f" have been purged from {self.ctx.channel.name}```"
            await self.message.edit(embed=self.embed,
                                    components=[Button(label="Approved", style=ButtonStyle.gray, disabled=True)])
            await self.message.clear_reactions()
        elif respond.component.label == "Reject":
            await self.message.clear_reactions()
            self.embed.title = "Rejected"
            self.embed.description = "```css\n [Clear Menu Canceled]```"
            self.embed.colour = discord.Color.blurple()
            await self.message.edit(embed=self.embed,
                                    components=[Button(label="Rejected", style=ButtonStyle.gray, disabled=True)])
        return None


class DefaultEmbed(object):
    """
    a DefaultEmbed object cause im lazy as fuck :/
    """

    def __init__(self, commandName: str, ctx: commands.Context):
        self.footer = f"Used at {ctx.message.created_at.strftime('%H:%M:%S')} by 🔹{ctx.author.display_name}🔹"
        self.footer_icon = ctx.author.avatar_url
        self.header = f"{commandName} Command"
        self.header_url = ctx.message.jump_url

    @classmethod
    def close(self):
        """
            returns a predefined Embed obeject for when a menu is closed
            :return:
            """
        return discord.Embed(title="", description="```css\nThis [Menu] has been [Closed]❌```",
                             colour=discord.Color.red())


class BotConfig(object):
    """
    Bot Config Object
    """

    def __init__(self, PATH: str):
        self.PATH = PATH
        self.operator_id = 0
        self.token = ""
        self.version = ""
        self.name = ""
        self.prefix = ""
        self.gif_apikey = ""
        self.slashguilds = []
        self.globalcounter = 0
        self.data = None

    def Load(self):
        """
        Loads The bots config to the BotConfig Object from the specified PATH.
        """
        with open(self.PATH, "r") as file:
            self.data = json.load(file)
            self.operator_id = self.data["moderator"]
            self.token = self.data["token"]
            self.prefix = self.data["prefix"]
            self.name = self.data["name"]
            self.gif_apikey = self.data["gif_api"]
            self.version = self.data["version"]
            self.slashguilds = self.data["slashguilds"]
            self.globalcounter = self.data["globalcounter"]

    def update(self, section: str, value):
        self.data[section] = value
        self.__setattr__(section, value)
        with open(self.PATH, "w") as file:
            file.write(json.dumps(self.data))


class HexConvertor():
    """
    Hex Convertor class, Lazy Stuff :/
    """

    def to_hex(str: str) -> str:
        """
        converts a ascii text to hexadecimal value
        :return str:
        """
        string = binascii.hexlify(str.encode())
        return string.decode()

    def from_hex(str: str):
        """
        converts a hexadcimal value to ascii text
        :return str:
        """
        try:
            string = binascii.unhexlify(str).decode()
            return string
        except binascii.Error:
            return "ERROR | Input was not a HexoDecimal Value!"


class HexMenu(menus.Menu):
    """
    Default Hexadecimal Menu for {Prefix}Hex
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=30.0)
        self.bot = bot

    async def send_initial_message(self, ctx: commands.Context, channel: discord.TextChannel):
        embeddf = DefaultEmbed("HEX", ctx)
        embed = discord.Embed(title="**What do you want to do?**", description="```css\n[Choose your option]```",
                              colour=discord.Color.random())
        embed.set_footer(text=embeddf.footer, icon_url=embeddf.footer_icon)
        embed.set_author(name=embeddf.header, url=embeddf.header_url)
        self.embed = embed
        self.message = await channel.send(embed=embed, components=[
            [Button(label="To Hex", style=ButtonStyle.green),
             Button(label="To ASCII", style=ButtonStyle.green),
             Button(label="Exit", style=ButtonStyle.gray)]])
        try:
            respond = await self.bot.wait_for("button_click", check=lambda i: i.user == self.ctx.author, timeout=20)
            await respond.respond(type=6)
            if respond.component.label == "To Hex":
                self.embed.description = "**Send the text that you want to `Hexlify` in this channel!**"
                self.embed.title = "**Text To Hex** Selected"
                self.embed.colour = discord.Color.red()
                await self.message.edit(embed=self.embed, components=[])
                text = await self.bot.wait_for('message', timeout=15,
                                               check=lambda message: message.author == self.ctx.author)
                self.embed.title = "`Your Hexlified Text is`**:**"
                self.embed.description = f"```fix\n{HexConvertor.to_hex(text.content)}```"
                self.embed.add_field(name="`Your Input Value`**:**", value=f"```css\n[{text.content}]```")
                self.embed.colour = discord.Color.green()
                await self.message.edit(embed=self.embed)
                await self.message.clear_reactions()
                await text.delete()
            elif respond.component.label == "To ASCII":
                self.embed.description = "**Send the Hexadecimal Value you want to `UnHexlify` in this channel!**"
                self.embed.title = "**Hex To Text** Selected"
                self.embed.colour = discord.Color.red()
                await self.message.edit(embed=self.embed, components=[])
                text = await self.bot.wait_for('message', timeout=15,
                                               check=lambda message: message.author == self.ctx.author)
                self.embed.title = "`Your UnHexlified Text is`**:**"
                self.embed.description = f"```fix\n{HexConvertor.from_hex(text.content)}```"
                self.embed.add_field(name="`Your Input Value`**:**", value=f"```css\n[{text.content}]```")
                self.embed.colour = discord.Color.green()
                await self.message.edit(embed=self.embed)
                await text.delete()
            elif respond.component.label == "Exit":
                await self.message.edit(components=[], embed=DefaultEmbed.close(),
                                        delete_after=7)
                await self.ctx.message.delete()
            return None
        except TimeoutError:
            await self.message.delete()
            await self.ctx.message.delete()
            raise TimeoutError()
