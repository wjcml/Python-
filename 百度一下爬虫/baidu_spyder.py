import requests
import re
from requests.exceptions import RequestException

def get_one_page(url):
	try:
		response=requests.get(url)
		response.encoding='utf-8'
		if response.status_code==200:
			return response.text
		return None
	except RequestsException:
		return None
	
def parse_one_page(html):
	pattern=re.compile('<div id="lg">.*?<img.*?class="index-logo-src" src="(.*?)".*?usemap="#mp">',re.S)
	item=re.findall(pattern, html)
	return item

def main():
	url='https://www.baidu.com/'
	html=get_one_page(url)
	item=parse_one_page(html)
	print(item)

if __name__=='__main__':
	main()
