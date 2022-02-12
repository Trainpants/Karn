import aiohttp
import asyncio
import json
import re

async def process_message(message):
    scryfall_expression = r"\[\[(.+)\]\]"
    scryfall_regex = re.compile(scryfall_expression)
    expression_match = scryfall_regex.match(message.content)
    if expression_match:
        card_name = expression_match.group(1)
        async with aiohttp.ClientSession() as session:
            params = {'q': card_name}
            async with session.get('https://api.scryfall.com/cards/search', params=params) as resp:
                if resp.status == 404:
                    await message.channel.send("Scryfall search:\nNo card found")
                    return
                
                deserialized_card = await resp.json()
                with open("last_scryfall_search.json","w") as search_results:
                    json.dump(deserialized_card,search_results)
                
                if deserialized_card['total_cards'] == 1:
                    card_image_uri = deserialized_card['data'][0]['image_uris']['normal']
                    await message.channel.send(card_image_uri)

                if deserialized_card['total_cards'] in range(2,6):
                    onetofive = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
                    output = "Scryfall search:\nDid you mean:\n"
                    for i in range(deserialized_card['total_cards']):
                        output += onetofive[i] + " " + deserialized_card['data'][i]['name'] + "\n"
                    message = await message.channel.send(output)
                    for k in range(deserialized_card['total_cards']):
                        await message.add_reaction(onetofive[k])

                if deserialized_card['total_cards'] > 5 :
                    results_message = await message.channel.send("Scryfall search:\n{} cards found. Be more specific".format(deserialized_card['total_cards']))
                    if deserialized_card['total_cards'] <= 50:
                        await results_message.add_reaction("📜")


async def process_reaction(reaction):
    if reaction.message.content.startswith("Scryfall search:"):
        if reaction.emoji == "📜":
            output = ""
            with open("last_scryfall_search.json","r") as last_search_results:
                searched_cards = json.load(last_search_results)
            for card in searched_cards['data']:
                output += card['name']+"\n"
            await reaction.message.channel.send(output)

        onetofive = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        if reaction.emoji in onetofive:
            cardnum = onetofive.index(reaction.emoji)
            with open("last_scryfall_search.json","r") as last_search_results:
                searched_cards = json.load(last_search_results)
            card_image_uri = searched_cards['data'][cardnum]['image_uris']['normal']
            await reaction.message.channel.send(card_image_uri)
