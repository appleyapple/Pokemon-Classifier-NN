import requests
import shutil
import os
import pandas as pd
from util import *


"""
Uses the API by pokeapi.co to scrape the follow Pokemon data:
    > ID
    > Name
    > Type(s)
    > Sprite image

The database currrently includes Pokemon #1-807 as of 18/06/2020.
Both primary and secondary types are extracted if they exist.
Only default sprites (male, female, front, back) are used during 
training; shiny sprites are excluded.
"""


print('Starting dataset creation...')


# Setup dataset directory tree
try:
    os.makedirs('../Dataset/Sprites')

except FileExistsError:
    print('Dataset directory already exists...')


# Ordered lists containing Pokemon data
ids = []
names = []
primary_types = []
secondary_types = []
sprites = []


# Extract necessary data from PokeAPI; one entry per sprite
print('Getting Pokemon data from PokeAPI...')

for pokemon_id in range(1, 50):

    data = fetch_data(pokemon_id)

    for sprite in SPRITE_TYPES:
        
        if data['sprites'][sprite] == None:
            continue

        else:
            img_name = process_image(pokemon_id, sprite, data['sprites'][sprite])
            
            add_id(data['id'], ids)
            add_name(data['name'], names)
            add_types(data['types'], primary_types, secondary_types)
            add_sprite(img_name, sprites)


# Create csv file
print('Creating dataset.csv...')

pokemon_dict = {
        'ID': ids,
        'Name' : names,
        'PrimaryType' : primary_types,
        'SecondaryType' : secondary_types,
        'Sprites' : sprites
}

df = pd.DataFrame(pokemon_dict)
df.to_csv('../Dataset/dataset.csv', index = False)

print('Complete.')

