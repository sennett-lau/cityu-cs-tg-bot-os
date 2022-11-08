import requests
import json
import random

def wantpokemon(update, context):
    poke_id = random.randrange(897) + 1
    r = requests.get('https://pokeapi.co/api/v2/pokemon/{}/'.format(poke_id))
    poke = json.loads(r.content)
    indefinite = 'an' if poke['types'][0]['type']['name'][0] in ['a', 'e', 'i', 'o', 'u'] else 'a'
    text = 'This is {},\n {} '.format(poke['name'], indefinite)
    for index, poketype in enumerate(poke['types']):
        if index > 0:
            text += ' & '
        text += poketype['type']['name']
    text += ' pokémon!'
    poke_id = str(poke_id).zfill(3)
    photo_url = 'https://assets.pokemon.com/assets/cms2/img/pokedex/detail/{}.png'.format(poke_id)
    context.bot.send_photo(chat_id=update.message.chat.id, photo=photo_url, caption=text)

