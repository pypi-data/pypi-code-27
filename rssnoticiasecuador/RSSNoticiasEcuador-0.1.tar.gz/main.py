import random
import feedparser

def tosp(date):
	date = date.replace('Mon','Lunes')
	date = date.replace('Tue','Martes')
	date = date.replace('Wed','Miércoles')
	date = date.replace('Thu','Jueves')
	date = date.replace('Fri','Viernes')
	date = date.replace('Sat','Sábado')
	date = date.replace('Sun','Domingo')

	return date

def showFeedsElUniverso(url):
	feedsList = []
	feeds = feedparser.parse(url)

	for entry in feeds['entries']:
		entryList = []
		entryList.append(feeds['feed']['title'])
		entryList.append(entry['title_detail']['value'])
		entryList.append(entry['link'])
		entryList.append(entry['summary_detail']['language'])
		entryList.append(entry['summary_detail']['value'])
		entryList.append(tosp(entry['published']))
		feedsList.append(entryList)
	return feedsList

def obtenerNoticias():

	urls = ['https://www.eluniverso.com/rss/destinos',
	'https://www.eluniverso.com/rss/mascotas',
	'https://www.eluniverso.com/rss/familia',
	'https://www.eluniverso.com/rss/nutrici%C3%B3n',
	'https://www.eluniverso.com/rss/cocina',
	'https://www.eluniverso.com/rss/gente.xml',
	'https://www.eluniverso.com/rss/espect%C3%A1culos',
	'https://www.eluniverso.com/rss/cine',
	'https://www.eluniverso.com/rss/futbol.xml',
	'https://www.eluniverso.com/rss/intercultural',
	'https://www.eluniverso.com/rss/internacional.xml',
	'https://www.eluniverso.com/rss/economia.xml',
	'https://www.eluniverso.com/rss/politica.xml',
	'https://www.eluniverso.com/rss/arte',
	'https://www.eluniverso.com/rss/redes-sociales',
	'https://www.eluniverso.com/rss/gastronomia',
	'https://www.eluniverso.com/rss/fitness',
	'https://www.eluniverso.com/rss/moda',
	'https://www.eluniverso.com/rss/belleza',
	'https://www.eluniverso.com/rss/compras']

	entries = []
	for url in urls:
		entries += showFeedsElUniverso(url)

	random.shuffle(entries)
	return entries

import eluniverso as u
print(u.obtenerNoticias())