#learn

import json
import os

async def process_learn(message):
    if message.content.startswith("?learn "):
        split_message = message.content.split(" ",2)
        if len(split_message) != 3:
            await message.channel.send("that didn't work")
            return
        mention, text = split_message[1], split_message[2]
        
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
        await message.channel.send("Okay, learned " + mention)

    if message.content.startswith("gimme "):
        pass







    