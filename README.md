# HUSK version 2.2 Update

**added (+):**

 > (+) support for the new `discord Buttons component`
 
 > (+) `sdk.husk_sdk.MemoryGame()` (not used rn, there for future uses)
 
 > (+) `{prefix}gbutton` , its a global button click counter for you and the bois to click.
 
 > (+) `{prefix}mafia`, only the bots ownenr can use it, its extremely unstable and its just here for future uses.
 
 > (+) `husk_sdk.BotConfig.update()` method to update and reload the config list.
 
 > (+) added `BotConfig.globalcounter` for `{prefix}gbutton`
 -----------
 **Modified (M):**
 
 > (M) changed the old config loading method, now its loaded only `one time` and its loaded into `bot.config`:
```py
config = husk_sdk.BotConfig(...); config.Load()
bot = commands.Bot(...)
bot.__setattr__("config", config)
```
> (M) there is no `husk_sdk.default_close()` any more, its moved and renamed to `husk_sdk.DefaultEmbed.close()`

> (M) `[HelpMenu, ClMenu, HexMenu]` are now button component based and they no longer operate on emojies and reactions

 
#### these are not all the changes tho i dont remember everything that i changed :/ , thats it for this update, the next one will contain some `GAMES` for people to play in discord including a pokemon game
if you look into the .gitignore file, youll see the games.py part, so stay tuned ;)
