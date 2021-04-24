import requests
from bs4 import BeautifulSoup

urls=[
    'https://wiki.guildwars2.com/wiki/Deldrimor_Steel_Ingot',
    'https://wiki.guildwars2.com/wiki/Carbonized_Mithrillium_Ingot',
    'https://wiki.guildwars2.com/wiki/Spiritwood_Plank',
    'https://wiki.guildwars2.com/wiki/Composite_Wood_Board',
    'https://wiki.guildwars2.com/wiki/Elonian_Leather_Square',
    'https://wiki.guildwars2.com/wiki/Blended_Leather_Sheet',
    'https://wiki.guildwars2.com/wiki/Bolt_of_Damask',
    'https://wiki.guildwars2.com/wiki/Gossamer_Stuffing',
    'https://wiki.guildwars2.com/wiki/Square_of_Vabbian_Silk'
]

urls_daily = [
    'https://wiki.guildwars2.com/wiki/Lump_of_Mithrillium',
    'https://wiki.guildwars2.com/wiki/Glob_of_Elder_Spirit_Residue',
    'https://wiki.guildwars2.com/wiki/Spool_of_Thick_Elonian_Cord',
    'https://wiki.guildwars2.com/wiki/Spool_of_Silk_Weaving_Thread'
]

def create_itens(urls):
    itens = []

    for url in urls:
        item = {
            'name': None,
            'id': None,
            'url': url,
            'api_price':None,
            'sellprice': None,
            'buyprice': None, 
            'recipe':None
        }

        get_item(url,item)

        itens.append(item)

    return itens


def get_item(url, item):

    gw2_wiki = requests.get(url)
    soup_page = BeautifulSoup(gw2_wiki.content,'html.parser')

    name = soup_page\
        .find('h1', class_="firstHeading")\
        .get_text()

    id = soup_page\
        .find(id="gamelink-1")\
        .get('data-id')

    recipe = soup_page\
    .find('span',{'class':'plainlinks'})\
    .find('a', recursive = False)\
    .get('href')

    recipe = 'https{}'.format(recipe)

    api_price = 'https://api.guildwars2.com/v2/commerce/prices?ids={}&wiki=1&lang=en'.format(id)
    sellprice, buyprice = get_api_price(api_price)


    item['name'] = name
    item['id'] = id
    item['api_price'] = api_price
    item['sellprice'] = sellprice
    item['buyprice'] = buyprice
    item['recipe'] = recipe

def get_api_price(url):
    response = requests.get(url)
    json = response.json()
    result = json[0]['sells']['unit_price']
    result2 = json[0]['buys']['unit_price']

    return result, result2

def check_recipe(url):
    print('hello world')


def print_list_dict(itens):
    for item in itens:
        for key, value in item.items():
            print(key, ' : ', value)
        print('--------')





def main():
    
    itens = create_itens(urls)
    print_list_dict(itens)




main()
