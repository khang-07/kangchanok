import sys
import music
sys.path.insert(0, "discord.py-self")
sys.path.insert(0, "discord.py-self_embed")

import discord
from discord.ext import commands
# import discord_self_embed
import json

with open("config.json", "r") as file:
    config = json.load(file)

token = config["token"]
prefix = config["prefix"]

bot = commands.Bot(command_prefix=prefix, self_bot=True)

#@bot.command()
#async def embed(ctx):
#   embed = discord_self_embed.Embed("Test Title", 
#      description="Very cool Description!", 
#    )
#    embed.set_author(f"{ctx.author}")

#    url = embed.generate_url(hide_url=True)
#    await ctx.send(url)

# takes array of str
def format(message):
    separated = "\n".join(map(str, message))
    return f"```{separated}```"

@bot.command()
async def msg(ctx, user: discord.Member, *, message):
    await user.send(message)
    print(f"Message Sent: {message} to {user.name} ({user.id})")

@bot.command()
async def ping(ctx):
    await ctx.send("pongers")
    print(f"pinged")

@bot.command()
# try except doesn't work here
async def liked(ctx, index=-1): 
    list = []
    await music.get_liked()
    with open("data.json", "r") as file:
        data = json.load(file)
    if (index != -1):
        i = int(index)
        await ctx.send("```" + data["liked"][i]["track"] + " : " + data["liked"][i]["artist"] + "```")
    else:
        for i, song in enumerate(data["liked"]):
            list.append(song["track"] + " : " + song["artist"])
        await ctx.send(format(list))

@bot.command()
async def playlist(ctx, *msgs):
    name = " ".join(map(str, msgs))
    if (name):
        await music.get_playlist(name)
        with open("data.json", "r") as file:
            data = json.load(file)
        await ctx.send(format(data["songs"]))
    else:
        await music.all_playlists()
        with open("data.json", "r") as file:
            data = json.load(file)
        await ctx.send(format(data["playlists"]))

@bot.command()
async def idk(ctx, *msgs):
    await ctx.send(type(msgs))
    await ctx.send(" ".join(map(str, msgs)))


bot.run(token)

# end = ctrl+C terminal