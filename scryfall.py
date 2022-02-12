import aiohttp
import asyncio

import re

async def process_message(message):
    scryfall_expression = r"\[\[(.+)\]\]"
    scryfall_regex = re.compile(scryfall_expression)
    expression_match = scryfall_regex.match(message.content)
    if expression_match:
        card_name = expression_match.group(1)
        async with aiohttp.ClientSession() as session:
            params = {'fuzzy': card_name}
            async with session.get('https://api.scryfall.com/cards/named', params=params) as resp:
                deserialized_card = await resp.json()
                card_image_uri = deserialized_card['image_uris']['normal']
                await message.channel.send(card_image_uri)
