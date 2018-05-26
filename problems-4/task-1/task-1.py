from bs4 import BeautifulSoup
from requests import get
from time import sleep
import sys

def start_article(URL):
	if is_wiki_page(URL) == -1:
		print("Is not an english wiki")
		sys.exit()
	return URL

def is_wiki_page(URL):
	wiki = "en.wikipedia"
	return URL.find(wiki)

def required_URL():
	return "https://en.wikipedia.org/wiki/Philosophy/" 

def next_article(URL, visited_articles):
	sleep(0.5)
	page = get(URL)
	link = get_link(BeautifulSoup(page.txt, "lxml"))
	path = link['href']
	print(path[6:], "article visited")
	if any(path in i for i in visited_articles):
		print ("Cycle")
		sys.exit()
	if URL == required_URL:
		print("Philosophy found")
		sys.exit()
	visited_articles.append(path)
	next_article("https://en.wikipedia.org" + path, visited_articles)


def get_link(soup):
	for i in soup.find_all('div', attrs={'class': 'mw-parser-output'}):
		return BeautifulSoup(str(i.find(['p', 'ul'], recursive=False)), "lxml").find(is_correct)
	return None

def is_correct(tag):
	if tag.name is not 'a':
		return False
	if tag.has_attr('class'):
		return False
	if not tag.has_attr('href') or not tag['href'].startswith('/'):
		return False
	return True


if len(sys.argv) < 2:
	print ("Need an URL")	
URL = ""
visited_articles = []
URL = start_article(sys.argv[1])
next_article(URL, visited_articles)
