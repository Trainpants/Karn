# lets make a discord bot
# https://docs.pycord.dev/en/master/index.html <- Pycord Docs

import discord
import json
import scryfall
import learn


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents = intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))



@client.event
async def on_message(message):
    
    if message.channel.name == dev_channel and is_dev_env != True:
        return
    if message.channel.name != dev_channel and is_dev_env == True:
        return

    await scryfall.process_message(message)

    await learn.learn_message(message)

    await learn.process_gimme(message)

    if message.author != client.user:
        if "?marco" in message.content.lower():
            await message.channel.send("Polo")


        if message.content.startswith("?echo ") or message.content.startswith("?say"):
            output = message.content
            output = output.split(" ",1)[1]
            await message.channel.send(output)


        if message.content.startswith("?spongecase "):
            string = message.content
            string = string.split(" ",1)[1]
            output = ""
            for index,letter in enumerate(string):
                if index % 2 == 0:
                    output += letter.lower()
                else:
                    output += letter.upper()
            await message.channel.send(output)


        if "good bot" in message.content.lower():
            await message.channel.send("\u263A") # messages smiley face


        if message.content.startswith("?plusreset"):
            if message.author.id == 256446512551297026:
                member_pluses = {}
                for member in message.guild.members:
                    member_pluses[member.id] = {"name": member.name, "score":100}
                with open("server_pluses.json","w") as plus_file:
                    json.dump(member_pluses, plus_file)
                await message.channel.send("Pluses reset")



@client.event
async def on_message_edit(before,after):
    if after.channel.name == dev_channel and is_dev_env != True:
        return
    if after.channel.name != dev_channel and is_dev_env == True:
        return

    if before.embeds == after.embeds:
        channel = after.channel
        await channel.send("Was the Grink there?",reference=after)



@client.event
async def on_reaction_add(reaction,user):
    if reaction.message.channel.name == dev_channel and is_dev_env != True:
        return
    if reaction.message.channel.name != dev_channel and is_dev_env == True:
        return

    if user != client.user:
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


client.run(config["bot_token"])