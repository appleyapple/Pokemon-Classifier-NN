import os
import pandas as pd
import numpy as np
from PIL import Image
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
    os.makedirs('../Dataset')

except FileExistsError:
    print('Dataset directory already exists...')
    print('Recreating dataset...')
    shutil.rmtree('../Dataset')

os.makedirs('../Dataset/Sprites')
os.makedirs('../Dataset/Train')
os.makedirs('../Dataset/Test')


# Ordered lists containing Pokemon data
ids = []
names = []
types = []
sprites = []


# Extract necessary data from PokeAPI; one entry per sprite
print('Getting Pokemon data & sprites from PokeAPI\nThis may take awhile...')

for pokemon_id in range(1, 50):

    data = fetch_data(pokemon_id)

    for sprite in SPRITE_TYPES:
        
        if data['sprites'][sprite] == None:
            continue

        else:
            img_name = process_image(pokemon_id, sprite, data['sprites'][sprite])
            
            add_id(data['id'], ids)
            add_name(data['name'], names)
            add_types(data['types'], types)
            add_sprite(img_name, sprites)


print('Creating dataset files...')

# Create csv files
pokemon_dict = {
        'ID': ids,
        'Name' : names,
        'Sprite' : sprites,
        'Types' : types
}

dataset = pd.DataFrame(pokemon_dict)
trainset = dataset.sample(frac=0.8)
testset = dataset.drop(trainset.index)

dataset.to_csv('../Dataset/dataset.csv', index = False, header=False)
trainset.to_csv('../Dataset/train.csv', index = False, header=False)
testset.to_csv('../Dataset/test.csv', index = False, header=False)


# Create train and test sprite folders
generate_train(trainset)
generate_test(testset)


print('Complete.')
