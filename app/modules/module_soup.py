import requests
from bs4 import BeautifulSoup

def get_web_data(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.content, 'html.parser')
	return soup