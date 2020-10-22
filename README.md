# Trigg's shit Icon bot

Automatically sets the icon of a discord server according to the current day.
Supposed to be ran daily (using something like windows task manager) to automate updating a server's icon.

Made because my friend forgets to change his server's icon for festivities like halloween or christmas.


# Requirements
Needs Python 3 and DiscordPy.

...What, you want an installation guide?

Well, you're shit out of luck mate, I'm a horrible teacher. Googling "Python" and "DiscordPy" got me places, though.

A Discord bot. Long story short, bots are discord accounts. You gotta make one yourself. Google "Discord bot token".


# Usage ~~(as if anyone will want to use it lmao)~~
When you first run it, it'll spit out 2 files:

- config.txt:
Put your discord bot's token and the ID of the server you wanna automate the icon of in here. **NOTE: Do not leak your token to anyone.** Bad people can do bad shit with it, which can get *you* banned because it's *your* bot and token. Uhhh, take this as a legal disclaimer or something. I dunno, I hate dealing with legal stuff.
- LastIcon.txt:
Don't touch it. Well, you're not *supposed* to touch it. But I'm not a cop. It just saves the last icon the bot used to prevent the bot from unnecessarily filling the audit logs.
