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

def create_itens(urls):
    itens = []

    for url in urls:
    	gw2_wiki = requests.get(url)
   		soup_page = BeautifulSoup(gw2_wiki.content,'html.parser')

   		name = get_item_name(soup_page)

		item = {
            'name': name,
            'id': None,
            'url': url,
            'sellprice': None,
            'buyprice': None, 
            'recipe':None
        }

        itens.append(item)
        set_names.append(name)

    return itens


def get_item_details(itens):
	for item in itens:

	    gw2_wiki = requests.get(item['url'])
	    soup_page = BeautifulSoup(gw2_wiki.content,'html.parser')

	    sellprice, buyprice = get_api_price(item['id'])
	    item['sellprice'] = sellprice
	    item['buyprice'] = buyprice
	    item['recipe'] = get_item_recipe(soup)

def get_item_name(soup):
	name = soup_page\
        .find('h1', class_="firstHeading")\
        .get_text()
    return name

def get_item_id(name):
	for key in item_json_list:
		if(name == key.get())
			return key.get()

def get_item_recipe(soup):
	soup_page\
    .find('span',{'class':'plainlinks'})\
    .find('a', recursive = False)\
    .get('href')
    recipe = 'https{}'.format(recipe)
    return recipe

def get_api_price(id):
	api_price_url = 'https://api.guildwars2.com/v2/commerce/prices?ids={}&wiki=1&lang=en'.format(id)
    response = requests.get(api_price_url)
    json = response.json()
    result = json[0]['sells']['unit_price']
    result2 = json[0]['buys']['unit_price']

    return result, result2

def get_all_ids(set):
	url_item_id = 'http://api.gw2tp.com/1/bulk/items-names.json'
	url_item_id_response = requests.get(url_item_id)
	json = requests.json()

	for item in ['items']
		if ''


	return


def item_id_list():


	return json


def get_recipe_list(item):
	recipe_list = []
	recipe_ingredients = {}
	url_recipe = item['recipe']

	recipe_request = url_recipe.requests
	recipe_soup = BeautifulSoup(recipe_request.content,'html.parser')
	soup_recipe_list = recipe.soup_page.\
	find('span',{'class':'small item-icon thumb-icon'})\
	.find('a', recursive = False)\
    .get('href')

def print_list_dict(itens):
    for item in itens:
        for key, value in item.items():
            print(key, ' : ', value)
        print('--------')


def main():
	set_names = set()
    itens = create_itens(urls)
    get_all_ids(set_names)

    print_list_dict(itens)






main()
