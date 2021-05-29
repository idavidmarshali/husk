from discord.ext import commands, menus
import discord, json, binascii, asyncio
import async_cleverbot as ac


# ///////////////////////
# Function Section ///
# /////////////////////
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
            self.pagelimit = 3 # limit to amount of commands in one menu page

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

        async def send_initial_message(self, ctx: commands.Context, channel: discord.TextChannel):
            self.embed = discord.Embed(title="__**HELP COMMAND**__")
            self.dict = self.formats()
            self.pages = len(self.dict.keys())
            self.currentpage = 1
            [self.embed.add_field(inline=False, name=f"`{command.name}`",
                                  value=f"```css\n[{self.helpObject.clean_prefix}{command.name} {command.signature}]\ndescription: {command.brief}```\n")
             for command in self.dict[self.currentpage]]
            embeddf = DefaultEmbed("Help", self.ctx)
            self.embed.set_footer(text=embeddf.footer, icon_url=embeddf.footer_icon)
            return await channel.send(embed=self.embed)

        @menus.button("◀")
        async def on_backward(self, payload):
            if self.currentpage >= 2:
                self.currentpage -= 1
                self.embed.clear_fields()
                [self.embed.add_field(inline=False, name=f"`{command.name}`",
                                      value=f"```css\n[{self.helpObject.clean_prefix}{command.name} {command.signature}]\ndescription: {command.brief}```\n")
                 for command in self.dict[self.currentpage]]
                await self.message.edit(embed=self.embed)


        @menus.button("▶")
        async def on_forward(self, payload):
            if self.currentpage <= self.pages:
                self.currentpage += 1
                self.embed.clear_fields()
                [self.embed.add_field(inline=False, name=f"`{command.name}`",
                                      value=f"```css\n[{self.helpObject.clean_prefix}{command.name} {command.signature}]\ndescription: {command.brief}```\n")
                 for command in self.dict[self.currentpage]]
                await self.message.edit(embed=self.embed)


        @menus.button("❌")
        async def on_close(self, payload):
            await self.message.edit(content="**MENU Closed!**", embed=None)
            await self.message.clear_reactions()
            await asyncio.sleep(5)
            await self.ctx.message.delete()
            await self.stop()

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
                              f"[{ctx.channel.name}] ?```\n✅- **Approve**\n❌- **Reject**")
        embed.set_footer(text=embeddf.footer, icon_url=embeddf.footer_icon)
        self.embed = embed
        return await ctx.send(embed=embed)

    @menus.button("✅")
    async def on_approve(self, payload):
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
        await self.message.edit(embed=self.embed)
        await self.message.clear_reactions()
        await self.stop()

    @menus.button("❌")
    async def on_reject(self, payload):
        await self.message.clear_reactions()
        self.embed.title = "```css\n[Clear Menu Canceled]```"
        self.embed.description = ""
        self.embed.colour = discord.Color.blurple()
        await self.message.edit(embed=self.embed)
        await self.stop()


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


class DefaultEmbed(object):
    """
    a DefaultEmbed object cause im lazy as fuck :/
    """

    def __init__(self, commandName: str, ctx: commands.Context):
        self.footer = f"Used at {ctx.message.created_at.strftime('%H:%M:%S')} by 🔹{ctx.author.display_name}🔹"
        self.footer_icon = ctx.author.avatar_url
        self.header = f"{commandName} Command"
        self.header_url = ctx.message.jump_url


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

    def Load(self):
        """
        Loads The bots config to the BotConfig Object from the specified PATH.
        """
        with open(self.PATH, "r") as file:
            data = json.load(file)
            self.operator_id = data["moderator"]
            self.token = data["token"]
            self.prefix = data["prefix"]
            self.name = data["name"]
            self.gif_apikey = data["gif_api"]
            self.version = data["version"]
            self.slashguilds = data["slashguilds"]


class HexMenu(menus.Menu):
    """
    Default Hexadecimal Menu for {Prefix}Hex
    """

    def __init__(self, bot: commands.Bot):
        super().__init__(timeout=30.0)
        self.bot = bot

    async def send_initial_message(self, ctx: commands.Context, channel: discord.TextChannel):
        embeddf = DefaultEmbed("HEX", ctx)
        embed = discord.Embed(title="**What do you want to do?**", description="1️⃣- `Text To Hex`\n2️⃣- `Hex to Text`"
                                                                               "\n❌- `Close The Menu`",
                              colour=discord.Color.random())
        embed.set_footer(text=embeddf.footer, icon_url=embeddf.footer_icon)
        embed.set_author(name=embeddf.header, url=embeddf.header_url)
        self.embed = embed
        return await channel.send(embed=embed)

    @menus.button("1️⃣")
    async def on_selection_text_to_hex(self, payload):
        await self.message.clear_reactions()
        self.embed.description = "**Send the text that you want to `Hexlify` in this channel!**"
        self.embed.title = "**Text To Hex** Selected"
        self.embed.colour = discord.Color.red()
        await self.message.edit(embed=self.embed)
        text = await self.bot.wait_for('message', timeout=15, check=lambda message: message.author == self.ctx.author)
        self.embed.title = "`Your Hexlified Text is`**:**"
        self.embed.description = f"```fix\n{HexConvertor.to_hex(text.content)}```"
        self.embed.add_field(name="`Your Input Value`**:**", value=f"```css\n[{text.content}]```")
        self.embed.colour = discord.Color.green()
        await self.message.edit(embed=self.embed)
        await self.message.clear_reactions()
        await text.delete()
        await self.stop()

    @menus.button("2️⃣")
    async def on_selection_hex_to_text(self, payload):
        await self.message.clear_reactions()
        self.embed.description = "**Send the Hexadecimal Value you want to `UnHexlify` in this channel!**"
        self.embed.title = "**Hex To Text** Selected"
        self.embed.colour = discord.Color.red()
        await self.message.edit(embed=self.embed)
        text = await self.bot.wait_for('message', timeout=15, check=lambda message: message.author == self.ctx.author)
        self.embed.title = "`Your UnHexlified Text is`**:**"
        self.embed.description = f"```fix\n{HexConvertor.from_hex(text.content)}```"
        self.embed.add_field(name="`Your Input Value`**:**", value=f"```css\n[{text.content}]```")
        self.embed.colour = discord.Color.green()
        await self.message.edit(embed=self.embed)
        await text.delete()
        await self.stop()

    @menus.button("❌")
    async def on_selection_exit(self, payload):
        await self.message.edit(content="```css\n[Menu Closed, Have a nice day! :)]```", embed=None, delete_after=7)
        await self.message.clear_reactions()
        await self.ctx.message.delete()
        await self.stop()
