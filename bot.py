from dotenv import load_dotenv
import os
from random import choice
from time import sleep
import datetime
import re

#below are the ones that aren't python builtins
from discordpy.ext import commands


configpath = "config.txt"
if not os.path.isfile(configpath): #why would someone delete it? no idea! but they could.
    with open(configpath, "w") as f:
        f.write("DISCORD_TOKEN=\nGUILD_ID=")


load_dotenv(configpath)

token = os.getenv("DISCORD_TOKEN")
if not token:
    print(f"The \"token\" field is empty - Please open \"{configpath}\" and put the discord bot token and Server ID in their respective fields.")
    exit()


try:
    guildID = int(os.getenv("GUILD_ID"))
    if not guildID:
        print("You had ONE job - To fill in the token AND the server ID you wanted it to change the icons for, AND YOU DIDN'T DO THE LATTER.")
        exit()

except ValueError:
    print("Dude, you put LETTERS on the Guild ID? Really? IT'S NUMBERS ONLY, NUMBNUT.")
    exit()


bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print("Bot is up. Let's see what today's icon will be...")

    global guildID
    for guild in bot.guilds: #why would it be in multiple? Idk.
        if guild.id == guildID: #but we're using just one.
            await dothing(guild)
            await bot.close()
            sleep(1) #gotta give the async loop time to kill itself else it (harmessly) screams an exception
            return
    print(f"The bot could not find a server with ID \"{guildID}\". Was it kicked? Was it never there? Did you write it wrong? Who knows! But probably the latter.")
    await bot.close()
    sleep(1)

current_year = datetime.date.today().year
def to_datetime(name:str) -> datetime.date:
    if(found := re.findall("[a-zA-Z]", name)):
        print(f"Not a number or \"Default\": ({', '.join(found)}) in \"{name}\". Skipping...")
        return

    when:list = name.split(".")
    if len(when) != 2:
        print(f"Invalid timestamp: \"{name}\". Skipping...")
        return
    when = [int(x) for x in when]
    
    #datetime is so needy that it REQUIRES a year, it doesn't default to something. laame.
    return datetime.date(year = current_year, month = when[1], day = when[0])

valid_file_endings = (".png", ".jpg", ".jpeg", ".gif")
def strip_file_ending(text):
    regex_text = "|".join([f"{x}$" for x in valid_file_endings])
    #or ".png$|.jpg$|.jpeg$|.gif$" but dynamic because... idk I like pain I guess
    #I may still have to hardcode this regex if this becomes a performance hog
    #That is, if for some reason this ends up having to scan like a thousand files for SOME REASON
    return re.sub(regex_text, '', text)

default = None
def scan(folder):
    matches = {"specific":[], "ranged":[]}
    for DirEntry in folder:
        if not DirEntry.name.endswith(valid_file_endings) or DirEntry.is_dir():
            continue

        name = strip_file_ending(DirEntry.name)
        a = name.split("-")

        if len(a) == 1: #gave us a specific day
            if a[0] == "Default":
                global default
                default = DirEntry
                continue

            if to_datetime(a[0]) == datetime.date.today():
                matches["specific"].append(DirEntry)

        elif len(a) == 2: #gave us a time range
            if to_datetime(a[0]) <= datetime.date.today() <= to_datetime(a[1]):
                matches["ranged"].append(DirEntry)

        else:
            print(f"Invalid time range: \"{name}\". Skipping...")

    return matches

    
def setIcon(DirEntry):
    global default
    if not DirEntry:
        print("setIcon() was called with a null DirEntry for fuck's sake")
        DirEntry = default
    isdefault = (DirEntry.name == "Default")

    try:
        IconBytes = open(DirEntry, "rb").read()

    except:
        if isdefault:
            print("Failed to read bytes from the Default file. Bailing out...")
            return

        else:
            print(f"Got an icon ({DirEntry.name}) for today but could not read any bytes. Using the default instead...")
            if not default:
                print("Couldn't find the default file, bailing out...")
                return
            return setIcon(default)

    if not IconBytes:
        if isdefault:
            print("Erm.. The default file is empty? Bailing out...")
            return
            
        else:
            print(f"Got an icon ({DirEntry.name}) for today but... The file is empty? Trying to use the default instead...")
            if not default:
                print("Couldn't find the default file, bailing out...")
                return
            return setIcon(default)

    return IconBytes

def lastIcon():
    with open("LastIcon.txt", "a"): #create it if it doesn't exist
        pass #imo this method is more stylish than using os.path.isfile() so I'm sticking with it

    with open("LastIcon.txt", "r") as file:
        return file.read() #errr, is this a security vulnerability?

def setLastIcon(name):
    with open("LastIcon.txt", "w") as file:
        file.write(name)

@bot.command()
async def dothing(guild):
    matches = scan(os.scandir("Icons"))

    icon = ""
    if matches["specific"]:
        icon = choice(matches["specific"])
    elif matches["ranged"]:
        icon = choice(matches["ranged"])

    if not icon:
        global default
        if not default:
            print("Could not find an icon for today and could not find a file named \"Default\". Bailing out...")
            return
        icon = default

    if icon.name == lastIcon():
        print("Today's icon seems to be the same as yesterday's icon, looks like my work here is already done!")
        return #no need to update

    IconBytes = setIcon(icon)
    if not IconBytes:
        return #seticon should have already given the proper warnings

    await guild.edit(reason="Automatic Icon Change, you're welcome.", icon = IconBytes)
    print(f"Set today's server icon to \"{icon.name}\"")
    setLastIcon(icon.name)


if __name__ == "__main__":
    bot.run(token)
