import aiohttp
import asyncio
import json
import re

async def process_message(message):
    scryfall_expression = r"\[\[(.+?)\]\]"
    scryfall_regex = re.compile(scryfall_expression)
    called_cards = re.findall(scryfall_regex, message.content)

    for card_name in called_cards:
        async with aiohttp.ClientSession() as session:
            params = {'q': card_name}
            async with session.get('https://api.scryfall.com/cards/search', params=params) as resp:
                if resp.status == 404:
                    await message.channel.send("Scryfall search: "+card_name+"\nNo card found")
                    return
                
                deserialized_card = await resp.json()
                
                if deserialized_card['total_cards'] == 1:
                    card_image_uri = deserialized_card['data'][0]['image_uris']['normal']
                    await message.channel.send(card_image_uri)

                if deserialized_card['total_cards'] in range(2,6):
                    onetofive = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                    output = "Scryfall search: " + card_name + "\nDid you mean:\n"
                    for i in range(deserialized_card['total_cards']):
                        output += onetofive[i] + " " + deserialized_card['data'][i]['name'] + "\n"
                    message = await message.channel.send(output)
                    for k in range(deserialized_card['total_cards']):
                        await message.add_reaction(onetofive[k])

                if deserialized_card['total_cards'] > 5 :
                    results_message = await message.channel.send("Scryfall search: " + card_name +"\n{} cards found. Be more specific".format(deserialized_card['total_cards']))
                    if deserialized_card['total_cards'] <= 50:
                        await results_message.add_reaction("📜")


async def process_reaction(reaction):
    if reaction.message.content.startswith("Scryfall search: "):
        async with aiohttp.ClientSession() as session:
            card_name = reaction.message.content.split("\n")[0].split(": ")[1]
            params = {'q': card_name}
            async with session.get('https://api.scryfall.com/cards/search', params=params) as resp:
                if resp.status == 404:
                    await message.channel.send("Scryfall search: "+card_name+"\nNo card found")
                    return
                    
                searched_cards = await resp.json()    
            
            if reaction.emoji == "📜":
                output = ""
                for card in searched_cards['data']:
                    output += card['name']+"\n"
                await reaction.message.channel.send(output)

            onetofive = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
            if reaction.emoji in onetofive:
                cardnum = onetofive.index(reaction.emoji)
                card_image_uri = searched_cards['data'][cardnum]['image_uris']['normal']
                await reaction.message.channel.send(card_image_uri)


