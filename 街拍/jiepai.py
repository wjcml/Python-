import requests
from requests.exceptions import RequestException
import re
from flask import json
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def get_page_index(offset,keyword):
	data={
		'offset': offset,
		'format': 'json',
		'keyword': keyword,
		'autoload': 'true',
		'count': '20',
		'cur_tab': 1
	}
	url='https://www.toutiao.com/search_content/?'+urlencode(data)
	try:
		response=requests.get(url)
		if response.status_code==200:
			return response.text
		return None
	except RequestException:
		print('请求索引页出错')
		return None

def parse_one_index(html):
	res_text=json.loads(html)		#将这个HTML转化成一个对象
	if 'data' in res_text.keys():
		for item in res_text.get('data'):
			yield item.get('article_url')

def get_one_detail(url):
	try:
		response=requests.get(url)
		if response.status_code==200:
			return response.text
		return None
	except RequestException:
		print('请求详情页出错',url)
		return None
		
def parse_one_detail(html):
	soup=BeautifulSoup(html,'lxml')
	title=soup.select('title')
	print(title)
	images_pattern=re.compile('var gallery=(.*?);',re.S)
	result=re.search(images_pattern, html)
	if result:
		print(result.group(1))

def main():
	html=get_page_index(0,'街拍')
	for url in parse_one_index(html):
		html=get_one_detail(url)
		if html:
			parse_one_detail(html)
	

if __name__ == '__main__':
	main()