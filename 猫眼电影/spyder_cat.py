import requests
from requests.exceptions import RequestException
import re
from flask import json
import mysql.connector
#抓取页面，判断是否成功，返回网页源代码
def get_one_page(url):
	headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"}
	try:
		response=requests.get(url,headers=headers)
		if response.status_code==200:
			return response.text
		return None
	except RequestException:
		return None

#正则表达式解析网页
def parse_one_page(html):
	pattern=re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
		+'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
		+'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
	items=re.findall(pattern,html)		# 返回的是匹配结果组成的列表，列表里面的每个元素都是有匹配规则中“()”匹配出的结果组成的数组
	for item in items:			 # 遍历数据通过yield将其构造成一个生成器，并返回
		yield{
			'indexs':item[0],
			'image':item[1],
			'title':item[2],
			'actor':item[3].strip()[3:],		#strip方法，去掉前3个字符（保留三字符后边的字符）
			'time':item[4].strip()[5:],		#strip方法，去掉前5个字符
			'score':item[5]+item[6]

		}

#将得到的数据写入到文件
def write_to_file(content):
	with open('result.txt','a',encoding='utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False)+'\n')		#
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

		_SQL="insert into cat(indexs,image,title,actor,time,score) values(%s,%s,%s,%s,%s,%s)"

		cursor.execute(_SQL,(content['indexs'],
							content['image'],
							content['title'],
							content['actor'],
							content['time'],
							content['score'],
			))

		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
		print(e)

def main(offset):
	url='http://maoyan.com/board/4?offset='+str(offset)
	html=get_one_page(url)
	for item in parse_one_page(html):
		#print(item)
		write_to_file(item)
		write_to_db(item)

if __name__=='__main__':
	for i in range(10):
		main(i*10)
