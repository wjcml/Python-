import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

def get_one_page(url):
	try:
		response=requests.get(url)
		if response.status_code==200:
			return response.text
		else:
			return None
	except Exception as e:
		return None

def parse_one_page(html):
	soup=BeautifulSoup(html,'lxml')
	texts=soup.find_all(class_='showtxt')
	return texts[0].text.replace('\xa0'*8,'\n\n')

def main(target):
	url=target
	html=get_one_page(url)
	texts=parse_one_page(html)
	print(texts)

if __name__ == '__main__':
	target='http://www.biqukan.com/1_1094/'
	response=requests.get(target)
	bf=BeautifulSoup(response.text,'lxml')
	topic=bf.find_all(class_='listmain')
	a=topic[0].find_all('a')
	print(a)