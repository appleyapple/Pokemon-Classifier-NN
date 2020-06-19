import requests

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

def build_url(id):

    if id not in range(1, MAX_ID + 1):
        raise ValueError('ID out of range')

    return '/'.join([BASE_URL, str(id)])

def export_csv(data):
    # Write id, name, type, 4 sprite urls to csv
    pass

url = build_url(1)
response = requests.get(url)
data = response.json()

id = data['id']
name = data['name']
types = data['types']
sprites = data['sprites']

print(id, name)
for i in range(len(types)):
    print(types[i]['type']['name'])
print(sprites['front_default'])
