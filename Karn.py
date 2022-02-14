# lets make a discord bot
# https://docs.pycord.dev/en/master/index.html <- Pycord Docs

import discord
import json
import scryfall
import learn
import re
import random
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = "?", intents = intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} as bot")



@bot.command()
async def plusreset(ctx):
    if ctx.channel.name == dev_channel and is_dev_env != True:
        return
    if ctx.channel.name != dev_channel and is_dev_env == True:
        return

    if ctx.author.id == 256446512551297026:
        member_pluses = {}
        for member in ctx.guild.members:
            member_pluses[member.id] = {"name": member.name, "score":100}
        with open("server_pluses.json","w") as plus_file:
            json.dump(member_pluses, plus_file)
        await ctx.send("Plusses reset")



@bot.command()
async def marco(ctx):
    if ctx.channel.name == dev_channel and is_dev_env != True:
        return
    if ctx.channel.name != dev_channel and is_dev_env == True:
        return

    ctx.send("polo")   



@bot.command()
async def roll(ctx, dice: str):
    if ctx.channel.name == dev_channel and is_dev_env != True:
        return
    if ctx.channel.name != dev_channel and is_dev_env == True:
        return

    if bool(re.match("\d*d\d+", dice)):
        rolls, sides = dice.split("d")
        if not rolls:
            rolls = "1"
        rolls = int(rolls)
        sides = int(sides)
        if rolls > 0 and sides > 0:
            for i in range(rolls):
                roll = random.randint(1,sides)
                await ctx.send(roll)
        else:
            await ctx.send("nice try, idiot")



@bot.command()
async def echo(ctx, *, arg):
    if ctx.channel.name == dev_channel and is_dev_env != True:
        return
    if ctx.channel.name != dev_channel and is_dev_env == True:
        return
    await ctx.send(arg)



@bot.command()
async def spongecase(ctx, *, arg):
    if ctx.channel.name == dev_channel and is_dev_env != True:
        return
    if ctx.channel.name != dev_channel and is_dev_env == True:
        return
    output = ""
    for index,letter in enumerate(arg):
        if index % 2 == 0:
            output += letter.lower()
        else:
            output += letter.upper()
    await ctx.send(output)



@bot.event
async def on_message(message):
    if message.channel.name == dev_channel and is_dev_env != True:
        return
    if message.channel.name != dev_channel and is_dev_env == True:
        return

    await scryfall.process_message(message)
    await learn.learn_message(message)
    await learn.process_gimme(message)

    if "good bot" in message.content.lower():
        await message.channel.send("\u263A") # messages smiley face

    await bot.process_commands(message)



@bot.event
async def on_message_edit(before,after):
    if after.channel.name == dev_channel and is_dev_env != True:
        return
    if after.channel.name != dev_channel and is_dev_env == True:
        return

    if before.embeds == after.embeds:
        channel = after.channel
        await channel.send("Was the Grink there?",reference=after)



@bot.event
async def on_reaction_add(reaction,user):
    if reaction.message.channel.name == dev_channel and is_dev_env != True:
        return
    if reaction.message.channel.name != dev_channel and is_dev_env == True:
        return

    channel = reaction.message.channel

    await scryfall.process_reaction(reaction)
    await learn.learn_reaction(reaction)

    if reaction.emoji == "\u2795": # plus
        if user == reaction.message.author:
            await channel.send("No self-plussing, that's gross.", reference = reaction.message)
        else:
            with open("server_pluses.json","r") as plus_file:
                member_pluses = json.load(plus_file)
            pluser = user.name
            plusee = reaction.message.author.name
            pluser_id = str(user.id)
            plusee_id = str(reaction.message.author.id)
            member_pluses[pluser_id]["score"] -= 1 # pluser loses one plus
            member_pluses[plusee_id]["score"] += 1 # plusee gains one
            output = plusee + " \U0001F53C " + str(member_pluses[plusee_id]["score"]) + " / " + str(member_pluses[pluser_id]["score"]) + " \U0001F53D " + pluser
            await channel.send(output, reference = reaction.message)
            with open("server_pluses.json","w") as plus_file:
                json.dump(member_pluses, plus_file)

    elif reaction.emoji == "\U0001F35E": # bread
        await reaction.message.add_reaction(reaction)





with open("config.json","r") as config_file:
    config = json.load(config_file)
is_dev_env = config["dev_environment"]
dev_channel = config["dev_channel"]

bot.run(config["bot_token"])