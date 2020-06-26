import os
import requests
import shutil
import pandas as pd
import numpy as np


MAX_ID = 807
BASE_URL = 'https://pokeapi.co/api/v2/pokemon'
SPRITE_TYPES = ['front_default', 'back_default', 'front_female', 'back_female']
POKEMON_TYPES = ['normal', 'fire', 'fighting', 'water', 'flying', 'grass',
                'poison', 'electric', 'ground', 'psychic', 'rock', 'ice', 'bug',
                'dragon', 'ghost', 'dark', 'steel', 'fairy']
NUM_TYPES = len(POKEMON_TYPES)


# Builds the URL containing Pokemon data specified by ID and then 
# requests it. Outputs a JSON file for further data extraction.
def fetch_data(id):

    if id not in range(1, MAX_ID + 1):
        raise ValueError('ID out of range')

    url = '/'.join([BASE_URL, str(id)])
    response = requests.get(url)

    return response.json()


# Downloads specified sprite images and formats the name to:
#       'id-sprite_type.png'
# Assumes ./Dataset/Sprites directory exists.
def process_image(id, sprite_type, url):

    img_name = str(id) + '-' + sprite_type
    img_path = '../Dataset/Sprites/' + img_name + '.png'
    response = requests.get(url, stream = True)

    if response.status_code == 200:

        response.raw.decode_content = True

        with open(img_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
    
    else:
        print('Image could not be retrieved')

    return img_name


# Copies training sprites to the train folder
def generate_train(train_df):

    for index, rows in train_df.iterrows():

        sprite_path = os.path.join('../Dataset/Sprites', rows.Sprite + '.png')
        shutil.copy(sprite_path, '../Dataset/Train')

    return 


# Copies test sprites to the test folder
def generate_test(test_df):

    for index, rows in test_df.iterrows():

        sprite_path = os.path.join('../Dataset/Sprites', rows.Sprite + '.png')
        shutil.copy(sprite_path, '../Dataset/Test')

    return 


# Wrapper functions for readability
def add_id(id, id_list):

    id_list.append(id)

    return


def add_name(name, name_list):

    name_list.append(name)

    return


def add_types(types, types_list):

    pokemon_types = [types[0]['type']['name']]

    if len(types) > 1:
        pokemon_types.append(types[1]['type']['name'])

    types_list.append(pokemon_types)

    return


def add_sprite(sprite_name, sprite_list):

    sprite_list.append(sprite_name)

    return


def append_png(file_name):
    return file_name + ".png"

