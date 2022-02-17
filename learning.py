#learning 
#(previously "learn.py", renamed to avoid conflict with ?learn command in main code)

import json
import os
import random


# Code section no longer necessary due to @bot.command formatting
# see: def learn()

#async def learn_message(message):
#    if message.content.startswith("?learn "):
#        split_message = message.content.split(" ",2)
#        if len(split_message) != 3:
#            await message.channel.send("that didn't work")
#            return
#        mention, text = split_message[1], split_message[2]
#        process_learn(mention,text)
#        await message.channel.send("Okay, learned " + mention)


# Code section moved to Karn.py to avoid await async bugs/nonsense

#async def learn_reaction(reaction):
#    if type(reaction.emoji) != str:
#        if reaction.emoji.name == "learn": 
#            mention = reaction.message.author.mention
#            mention = mention[0:2]+"!"+mention[2:]
#            text = reaction.message.content
#            process_learn(mention,text)
#            await reaction.message.channel.send("Okay, learned " + mention)



async def process_learn(mention,text):
    if not os.path.exists("learns.json"):
        with open("learns.json","w") as learn_file:
            json.dump({},learn_file)

    with open("learns.json","r") as learn_file:
        learns = json.load(learn_file)

    if mention not in learns:
        learns[mention] = [text]
    else:
        learns[mention].append(text)

    with open("learns.json","w") as learn_file:
        json.dump(learns, learn_file)



async def process_gimme(message):
    if message.content.startswith("gimme "):
        split_message = message.content.split()
        mention = split_message[1].strip()
        with open("learns.json","r") as learn_file:
            learn_dict = json.load(learn_file)
        if mention in learn_dict:
            await message.channel.send(random.choice(learn_dict[mention]))


