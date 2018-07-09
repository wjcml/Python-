import requests
from requests.exceptions import RequestException
import re
from flask import json
import mysql.connector

def get_one_page(url):
	try:
		response=requests.get(url)
		if response.status_code==200:
			return response.text
		return None
	except RequestException:
		return None

def parse_one_page(html):
	pattern=re.compile('<table width=".*?src="(.*?)".*?class="pl">(.*?)</p>'
		+'.*?<span class="rating_nums">(.*?)</span>.*?class="pl">.*?</span>',re.S)
	items=re.findall(pattern, html)
	for item in items:
		yield{
		'img':item[0],
		'actor':item[1].split("/"),
		'score':item[2]
		}

def write_to_file(content):
	with open("douban_movie.txt","a",encoding="utf-8") as f:
		f.write(json.dumps(content,ensure_ascii=False)+'\n')
		f.close()

def write_to_db(content):
	try:
		dbconfig={
		'host':'127.0.0.1',
		'user':'root',
		'password':'',
		'database':'test'
		}

		conn=mysql.connector.connect(**dbconfig)
		cursor=conn.cursor()

		_SQL="""insert into doubanmv
		(img,actor,score)
		values
		(%s,%s,%s)"""

		cursor.execute(_SQL,(content['img'],
							content['actor'][0],
							content['score'],
			))

		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
		raise e


def main():
	url='https://movie.douban.com/chart'
	html=get_one_page(url)
	for item in parse_one_page(html):
		#print(item)
		write_to_file(item)
		write_to_db(item)
	

if __name__=='__main__':
	main()