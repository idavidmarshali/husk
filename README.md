# HUSK Update - V2.1  - SlashCommands
**Genral change **: Added `slash commands` in `cogs/slashcommands.py`

Slash commands can currently *only* be used in guilds : `555067760703569960,801555851188895774`

# New SlashCommands are :

1. /hentai `optional[hidden?]`
2. /check `user`
3. /moveall
4. /muteall
5. /unmuteall
6. /clear `amount` `optional[user]`
7. /gif `category`
--------------

1. changed the check command so now it wont show `guild.default_role` as one of the members roles

2. changed the unmuteall command so now it `ignores the ctx.author`

3. added `getgifs` func to the sdk cause im lazy :/

4. added `slashguilds` parameter to `BotConfig()` and `bot.json`

5. minor changes to some commands.

6. Took out the tenor api token from the bots `gifs.py` cog XD
