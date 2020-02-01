import os
import json 
import requests
from bs4 import BeautifulSoup

GOOGLE_IMAGE = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
usr_agent = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

data_file = json.load(open('data.json','r'))
files = list(data_file.keys())

for SAVE_FOLDER in files:
	if not os.path.exists(SAVE_FOLDER):
		os.mkdir(SAVE_FOLDER)
	n_images = 100

	print('Start searching...',SAVE_FOLDER)

	searchurl = GOOGLE_IMAGE + 'q=' + SAVE_FOLDER.replace("_"," ")
	print(searchurl)

	# request url, without usr_agent the permission gets denied
	response = requests.get(searchurl, headers=usr_agent,timeout=20)
	html = response.text

	soup = BeautifulSoup(html, 'html.parser')
	results = soup.findAll('div', {'class': 'rg_meta'}, limit=n_images)

	imagelinks= []
	for re in results:
		text = re.text 
		text_dict= json.loads(text) 
		link = text_dict['ou']
		# image_type = text_dict['ity']
		imagelinks.append(link)

	print(f'found {len(imagelinks)} images')
	print('Start downloading...')

	for i, imagelink in enumerate(imagelinks):
		try:
			response = requests.get(imagelink)

			imagename = SAVE_FOLDER + '/' + str(i+1) + '.jpg'
			with open(imagename, 'wb') as file:
				file.write(response.content)
		except Exception as e:
			print("Error!!!",e)
	print('Done')
