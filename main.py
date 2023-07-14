import sys
import music
import asyncio
import nacl
sys.path.insert(0, "discord.py-self")

import discord
from discord.ext import commands
import json

with open("config.json", "r") as file:
    config = json.load(file)

token = config["token"]
prefix = config["prefix"]

bot = commands.Bot(command_prefix=prefix, self_bot=True)
"""
# takes array of str
def format(message):
    return "\n".join(map(str, message))

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
    await asyncio.sleep(5)
    if (index != -1):
        i = int(index)
        await ctx.send("```" + data["liked"][i]["track"] + " : " + data["liked"][i]["artist"] + "```")
    else:
        for i, song in enumerate(data["liked"]):
            list.append(song["track"] + " : " + song["artist"])
        await ctx.send(format(list))

@bot.command()
async def playlist(ctx, *msgs):
    print("starting")
    await asyncio.sleep(5)
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
    async with ctx.typing():
        await asyncio.sleep(5)
    await ctx.send(type(msgs))
    await ctx.send(" ".join(map(str, msgs)))

@bot.command()
async def join(ctx, *msgs):
    channel = " ".join(map(str, msgs))
    print("starting")
    await asyncio.sleep(5)
    for i, vc in enumerate(ctx.guild.voice_channels):
        if (vc.name == channel):
            await vc.connect()
    print("end")

@bot.command()
async def leave(ctx):
    print("starting")
    await asyncio.sleep(5)
    await ctx.guild.voice_client.disconnect()
    print("end")
"""

@bot.event
async def on_message(ctx):
    message = ctx.content.split(" ")
    if (ctx.author.id == 1128221831963361370 or ctx.author.id == 708191305322332210 or ctx.author.id == 532405312997687298):
        if ("play" in message):
            print("starting...")
            index = message.index("play") + 1
            await music.search(message[index:])
            print("finished!")
        

bot.run(token)

# end = ctrl+C terminal 