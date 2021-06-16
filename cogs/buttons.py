from discord.ext import commands, tasks
from discord_components import Button, ButtonStyle, Interaction
import discord, asyncio, random
from sdk import husk_sdk
import time



class buttoncommands(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.globalcounter = bot.config.globalcounter
        self.gcounterUpdater.start() #Starts the Global Click Counter AutoSave TASK

    @commands.command(name="gbutton", description="a Global Button Click Counter, as an stupid game :)")
    async def gbutton(self, ctx):
        initialEmbed=discord.Embed(title="Global Click Counter",colour=discord.Color.random(), description="```css\nhere is a little game, click the [red button] as much as you can :)```\n_if you got `interaction failed`, dont worry, its normal_\nThe Counter Updates every `3 Seconds`").set_footer(text="This Menu Will Automatically Timeout after 5 Minutes")
        msg = await ctx.send(embed=initialEmbed, components=[[Button(label="CLICK ME", style=ButtonStyle.red), Button(label=f"{self.globalcounter} clicks till now",disabled=True)]])
        ct = time.time()
        call_time = 4
        while time.time() - ct <= 300:
            if time.time() - call_time >= 3:
                call_time = time.time()
                await msg.edit(components=[[Button(label="CLICK ME", style=ButtonStyle.red),
                                            Button(label=f"{self.globalcounter} clicks till now", disabled=True)]])
            await msg.edit(components=[[Button(label="CLICK ME", style=ButtonStyle.red), Button(label=f"{self.globalcounter} clicks till now",disabled=True)]])
            respond = await self.bot.wait_for("button_click")
            await respond.respond(type=6)
            self.globalcounter += 1
        await msg.edit(embed=husk_sdk.DefaultEmbed.close())
        return
    @tasks.loop(seconds=60)
    async def gcounterUpdater(self):
        self.bot.config.update("globalcounter", self.globalcounter)


    @commands.command(name="mafia", description="Owner Only, for Mafia")
    @commands.is_owner()
    async def mafia(self, ctx):
        embed = discord.Embed(title="Mafia Menu", description="do you want to start a Mafia game?",
                              colour=discord.Color.dark_blue())
        main_message = await ctx.send(embed=embed, components=[
            [Button(label="Yes", style=ButtonStyle.green), Button(label="No", style=ButtonStyle.red)]])
        respond = await self.bot.wait_for("button_click", check=lambda i: i.user == ctx.author)
        await respond.respond(type=6)
        if respond.component.label == "Yes":
            joined_list = []
            embed.title, embed.description = "Mafia Game Started", f"**Current Game GOD : **{ctx.author.mention}\nCurrent Game Stat: `Waiting For Players`\n```css\nPlease click on [JoinGame] if you want to play!``` "
            await main_message.edit(embed=embed, components=[[Button(label="JoinGame", style=ButtonStyle.blue),
                                                             Button(label="Give Roles", style=ButtonStyle.gray)]],
                                    delete_after=10)

            def check(event):
                if event.component.label == "Give Roles":
                    if event.author == ctx.author:
                        return True
                    return False
                return (
                            event.user not in joined_list and event.user in ctx.author.voice.channel.members) if event.user != ctx.author else False

            playerList = []
            while True:
                respond = await self.bot.wait_for("button_click", check=lambda i : check(i))
                await respond.respond(type=6)
                if respond.component.label == "JoinGame":
                    joined_list.append(respond.user)
                    playerList.append(respond.user)
                    embed.add_field(name="💢〰〰💢", value=f"{respond.user.mention}", inline=True)
                    await main_message.edit(embed=embed)
                elif respond.component.label == "Give Roles":
                    break

            embed.description = f"**Current Game GOD : **{ctx.author.mention}\nCurrent Game Stat: `Giving Roles`"
            embed.clear_fields()
            embed.add_field(name="Current Players:", value="".join([member.mention for member in joined_list]))
            await main_message.edit(embed=embed, components=[Button(label="END THE GAME", style=ButtonStyle.red)])
            mafia, city, specialRoles = [], [], []

            if len(joined_list) >= 10:
                specialRoles = ["Mafia Boss", "Doctor", "Detective"]
                mafiaBosschoice = random.choice(joined_list)
                await mafiaBosschoice.send("**MAFIA GAME**\n\n You Are a `Mafia Boss`")
                joined_list.remove(mafiaBosschoice)
                mafia.append(mafiaBosschoice)
                detectiveChoice = random.choice(joined_list)
                await detectiveChoice.send("**MAFIA GAME**\n\n You Are a `Detective`")
                joined_list.remove(detectiveChoice)
                doctorChoice = random.choice(joined_list)
                await doctorChoice.send("**MAFIA GAME**\n\n You Are a `Doctor`")
                joined_list.remove(doctorChoice)
                city.append(doctorChoice)
                city.append(detectiveChoice)
                # about 2/3 of the city is citizen, 1/3 mafia (DOCTOR-MAFIA BOSS-Detective)
            elif 7 <= len(joined_list) < 10:
                specialRoles = ["Mafia Boss", "Detective"]
                mafiaBosschoice = random.choice(joined_list)
                await mafiaBosschoice.send("**MAFIA GAME**\n\n You Are a `Mafia Boss`")
                joined_list.remove(mafiaBosschoice)
                mafia.append(mafiaBosschoice)
                detectiveChoice = random.choice(joined_list)
                await detectiveChoice.send("**MAFIA GAME**\n\n You Are a `Detective`")
                city.append(detectiveChoice)
                # MAFIA BOSS - DETECTIVE
            elif len(joined_list) < 7:
                specialRoles = ["Mafia Boss"]
                mafiaBosschoice = random.choice(joined_list)
                await mafiaBosschoice.send("**MAFIA GAME**\n\n You Are a `Mafia Boss`")
                joined_list.remove(mafiaBosschoice)
                mafia.append(mafiaBosschoice)
                # ONLY MAFIA BOSS

            for _ in range(round(len(joined_list) / 3)):
                choice = random.choice(joined_list)
                await choice.send("**MAFIA GAME**\n\n You Are a `Normal Mafia`")
                joined_list.remove(choice)
                mafia.append(choice)
            for _ in range(len(joined_list)):
                choice = random.choice(joined_list)
                await choice.send("**MAFIA GAME**\n\n You Are a `Normal Citizen`")
                joined_list.remove(choice)
                city.append(choice)
            embed.description = f"**Current Game GOD : **{ctx.author.mention}\nCurrent Game Stat: `STARTED`\n" \
                                f"**Availabel Roles : {''.join(f'`{role}`' for role in specialRoles)}**"
            """def get_actionrow(playerlist):
                currentRow = 0
                actionrow = []
                for player in playerlist:
                    limit = round(len(playerList) / 4)
                    [actionrow.append([]) for _ in range(limit+1)]
                    if len(actionrow[currentRow]) < 4:
                        print("hey")
                        actionrow[currentRow].append(
                            Button(label=f"{player.name}", style=ButtonStyle.red, id=f"{player.id}"))
                    currentRow += 1

                return actionrow"""
            dead_people=[]
            await main_message.edit(embed=embed, components=[
                [Button(label="END THE GAME", style=ButtonStyle.red, id="end"),
                 Button(label="Mute All", style=ButtonStyle.gray, id="mute"),
                 Button(label="UnMute All", style=ButtonStyle.gray, id="unmute")]])
            while True:
                respond = await self.bot.wait_for("button_click", check=lambda i: i.user==ctx.author)
                await respond.respond(type=6)
                ids = respond.component.id
                if ids=="exit":
                    break
                elif ids == "mute":
                    command = self.bot.get_command("muteall")
                    await command(ctx)
                elif ids == "unmute":
                    command = self.bot.get_command("unmuteall")
                    await command(ctx)
                elif [member if member.id == int(ids) else False for member in playerList][0]:
                    player = [member if member.id == int(ids) else None for member in playerList]
                    dead_people.append(player[0])
                    [playerList.remove(member) if member.id == int(ids) else None for member in playerList]
                    embed.clear_fields()
                    embed.add_field(name="Current Players:", value="".join([member.mention for member in playerList]))
                    embed.add_field(name="Dead People:", value="".join([member.mention for member in dead_people]))
                    await main_message.edit(components=[
                [Button(label="END THE GAME", style=ButtonStyle.red, id="end"),
                 Button(label="Mute All", style=ButtonStyle.gray, id="mute"),
                 Button(label="UnMute All", style=ButtonStyle.gray, id="unmute")]])
            return await main_message.edit(embed=husk_sdk.DefaultEmbed.close(), components=[])
        elif respond.component.label == "No":
            await main_message.edit(embed=husk_sdk.DefaultEmbed.close(), components=[], delete_after=10)


def setup(bot):
    bot.add_cog(buttoncommands(bot))
    print("buttons.py loaded")
