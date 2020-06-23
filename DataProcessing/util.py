import requests
import shutil
import os
import pandas as pd


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
#       'id-sprite_type.png'
# Assumes ./Dataset/Sprites directory exists.
def process_image(id, sprite_type, url):

    img_name = str(id) + '-' + sprite_type
    img_path = '../Dataset/Sprites/' + img_name
    response = requests.get(url, stream = True)

    if response.status_code == 200:

        response.raw.decode_content = True

        with open(img_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
    
    else:
        print('Image could not be retrieved')

    return img_name


# Wrapper functions for readability
def add_id(id, id_list):
    id_list.append(id)
    return


def add_name(name, name_list):
    name_list.append(name)
    return


def add_types(types, primary_type_list, secondary_type_list):

    primary_type_list.append(types[0]['type']['name'])

    if len(types) > 1:
        secondary_type_list.append(types[1]['type']['name'])
    else:
        secondary_type_list.append(None)

    return


def add_sprite(sprite_name, sprite_list):
    sprite_list.append(sprite_name)
    return
