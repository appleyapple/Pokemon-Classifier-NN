import requests
import os
import pandas

"""
Uses the API by pokeapi.co to scrape the follow Pokemon data:
    > ID
    > Name
    > Type(s)
    > Sprite URL(s)

The database currrently includes Pokemon #1-807 as of 18/06/2020.
Both primary and secondary types are extracted if they exist.
Only default sprites (male, female, front, back) are used during 
training; shiny sprites are excluded.
"""

MAX_ID = 807
BASE_URL = 'https://pokeapi.co/api/v2/pokemon'
SPRITE_TYPES = ['front_default', 'back_default', 'front_female', 'back_female']


# Builds the URL containing Pokemon data specified by ID and then 
# requests it. Outputs a JSON file for further data extraction.
def fetch_data(id):

    if id not in range(1, MAX_ID + 1):
        raise ValueError('ID out of range')

    url = '/'.join([BASE_URL, str(id)])
    response = requests.get(url)

    return response.json()


# Downloads specified sprite images and formats the name to:
#       'id-sprite#.png'
#   ex: bulbasaur back_default sprite
#       '1-2.png'
def process_image(id, url):
    pass


# Write all Pokemon id, name, types, 4 sprite urls to a csv file.
# Creates 'Dataset' folder which contains the csv file if it does
# not already exist.
def export_csv(data):

    try:
        os.makedirs('Dataset')
    except FileExistsError:
        print('Dataset directory already exists')

    df = pandas.DataFrame(data)
    df.explode('Sprites')
    df.to_csv('./Dataset/dataset.csv', index = False)

    return

id = []
name = []
primary_type = []
secondary_type = []
sprites = []

for pokemon_id in range(1, 9, 2):

    data = fetch_data(pokemon_id)

    id.append(data['id'])
    name.append(data['name'])
    primary_type.append(data['types'][0]['type']['name'])

    if len(data['types']) > 1:
        secondary_type.append(data['types'][1]['type']['name'])
    else:
        secondary_type.append(None)
    
    sprite_list = []
    for sprite in SPRITE_TYPES:
        if data['sprites'][sprite] == None:
            continue
        else:
            sprite_list.append(data['sprites'][sprite])
    sprites.append(sprite_list)
    
# print(id, name, primary_type, secondary_type, sprites)
# print(len(id), len(name), len(primary_type), len(secondary_type), len(sprites))

pokemon_dict = {
        'ID': id,
        'Name' : name,
        'Primary Type' : primary_type,
        'Seconary Type' : secondary_type,
        'Sprites' : sprites,
}

export_csv(pokemon_dict)
