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

def create_items(urls,json):
	items = []

	for url in urls:
		gw2_wiki = requests.get(url)
		soup_page = BeautifulSoup(gw2_wiki.content,'html.parser')

		name = get_item_name(soup_page)
		id = get_id(name,json)
		sellprice, buyprice = get_api_price(id)
		recipe_url = get_item_recipe_url(soup_page)
		subitem = get_subitem(soup_page)

		item = {
			'name': name,
			'id': id,
			'url': url,
			'sellprice': sellprice,
			'buyprice': buyprice,
			'recipe_url': recipe_url,
			'subitem': subitem
			}
		items.append(item)
	return items

def get_item_name(soup):
	name = soup\
		.find('h1', class_="firstHeading")\
		.get_text()
	return name

def get_item_recipe_url(soup):
	recipe = soup\
	.find('span',{'class':'plainlinks'})\
	.find('a', recursive = False)\
	.get('href')
	recipe = 'https:{}'.format(recipe)
	return recipe

def get_api_price(id):
	api_price_url = 'https://api.guildwars2.com/v2/commerce/prices?ids={}&wiki=1&lang=en'.format(id)
	response = requests.get(api_price_url)
	json = response.json()
	result = json[0]['sells']['unit_price']
	result2 = json[0]['buys']['unit_price']

	return result, result2

def get_json_id_list():
	url_item_id = 'http://api.gw2tp.com/1/bulk/items-names.json'
	url_item_id_response = requests.get(url_item_id)
	json_id_list = url_item_id_response.json()

	return json_id_list

def get_id(name,json):

	for key, dkey in json.items():
		for item in dkey:
			if (item[1] == name):
				return item[0]

def get_recipe(item,json):
	recipe_ingredients = {}
	url_recipe = item['recipe_url']
	recipe_request =requests.get(url_recipe)
	recipe_soup = BeautifulSoup(recipe_request.content,'html.parser')
	soup_recipe_list = recipe_soup\
	.find('tbody')
	soup_recipe_name = soup_recipe_list.find_all('span',{'class':'small item-icon thumb-icon'})
	soup_recipe_quantity = soup_recipe_list.find_all('tr',{'class':'tptotal'})
	zip_recipe = zip(soup_recipe_name,soup_recipe_quantity)
	index = 0

	for element1, element2 in zip_recipe:
		soup_recipe_name[index] = element1.find('a').get('title')
		soup_recipe_quantity[index] = element2.get('data-qty') 
		recipe_ingredients[get_id(soup_recipe_name[index],json)] = [soup_recipe_name[index],soup_recipe_quantity[index]]
		index += 1
		
	return recipe_ingredients

def get_all_recipes(items,json):
	recipe_list = []

	for item in items:
		recipe_ingredients = get_recipe(item,json)
		recipe_list.append(recipe_ingredients)

	return recipe_list

def get_specific_recipe(url):
   
	recipe_request = requests.get(url)
	recipe_soup = BeautifulSoup(recipe_request.content,'html.parser')
	soup_recipe_list = recipe_soup\
	.find('tbody')

	soup_recipe_name = soup_recipe_list.find_all('span',{'class':'small item-icon thumb-icon'})
	soup_recipe_quantity = soup_recipe_list.find_all('tr',{'class':'tptotal'})

	zip_object = zip(soup_recipe_name,soup_recipe_quantity)

	index = 0
	for element1, element2 in zip_object:
		soup_recipe_name[index] = element1.find('a').get('title')
		soup_recipe_quantity[index] = element2.get('data-qty')

		index += 1

def get_subitem(soup):
	subitem_name_list = soup\
	.find('div', class_ = 'ingredients')\
	.find_all('span',{'class':'small item-icon thumb-icon'})\

	for subitem in subitem_name_list:

		subitem_name = subitem.find('a').get('title')

		if(subitem_name == 'Lump of Mithrillium'):
			return 'Lump of Mithrillium'

		if (subitem_name == 'Glob of Elder Spirit Residue'):
			return 'Glob of Elder Spirit Residue'

		if (subitem_name == 'Spool of Thick Elonian Cord'):
			return 'Spool of Thick Elonian Cord'

		if (subitem_name == 'Spool of Silk Weaving Thread'):
			return 'Spool of Silk Weaving Thread'


def print_list_dict(items):
	for item in items:
		for key, value in item.items():
			print(key, ' : ', value)
		print('--------')

def print_dict(item):
	for key,value in item.items():
		print(key, ' : ', value)
	print('--------')

def main():
	json_id_list = get_json_id_list()
	items = create_items(urls,json_id_list)
	recipes = get_all_recipes(items,json_id_list)
	print_list_dict(items)
	print('Lista de Recipes')
main()
