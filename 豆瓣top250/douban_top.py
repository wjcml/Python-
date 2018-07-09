import requests
from requests.exceptions import RequestException
import re
from flask import json
import mysql.connector
#请求目标网页，看是否访问成功，成功则返回网页源代码
def get_one_page(url):
	try:
		response=requests.get(url)
		if response.status_code==200:
			return response.text
		return None
	except RequestException:
		return None
#通过正则表达式解析网页，并以字典的形式返回
def parse_one_page(html):
	pattern=re.compile('<div class="item">.*?<em.*?>(.*?)</em>.*?src="(.*?)".*?<a href="(.*?)">.*?'		#正则表达式
		+'<span class="title">(.*?)</span>.*?="other">&nbsp;/&nbsp;(.*?)</span>.*?导演:(.*?)&nbsp;'
		+'&nbsp;&nbsp;.*?<br>.*?(\d+)&nbsp;/&nbsp;(.*?)&nbsp;/&nbsp;(.*?)</p>.*?="v:average">'
		+'(.*?)</span>.*?<span>(.*?)</span>.*?="inq">(.*?)</span>',re.S)
	items=re.findall(pattern, html)
	for item in items:		 # 遍历数据通过yield将其构造成一个生成器，并返回
		yield{
		'indexs':item[0],
		'image':item[1],
		'url':item[2].strip()[:-8],
		'title':item[3],
		'other':item[4],
		'director':item[5],
		'time':item[6],
		'country':item[7],
		'type':item[8],
		'score':item[9],
		'commentor':item[10],
		'topic':item[11]
		}
#将捕获到的数据写入TXT文件
def write_to_file(content):
	with open("douban_top.txt","a",encoding="utf-8") as f:
		f.write(json.dumps(content,ensure_ascii=False)+'\n')
		f.close()

#将捕获到的数据写入数据库
def write_to_DB(content):
	try:
		#MySQL连接属性
		dbconfig={
		'host':'127.0.0.1',
		'user':'root',
		'password':'',
		'database':'test',
		}
		#创建连接和游标
		conn=mysql.connector.connect(**dbconfig)
		cursor=conn.cursor()

		_SQL="""insert into log
		(indexs,url,title,director,time,score)
		values
		(%s,%s,%s,%s,%s,%s)"""
		#写入数据
		cursor.execute(_SQL,(content['indexs'],
							 content['url'],
							 content['title'],
							 content['director'],
							 content['time'],
							 content['score'],))
		#关闭连接和游标
		conn.commit()
		cursor.close()
		conn.close()
	except Exception as e:
		print(e)




def main(start):
	url='https://movie.douban.com/top250'+'?start='+str(start)+'&filter'   #豆瓣电影排行榜地址
	html=get_one_page(url)
	for item in parse_one_page(html):
		write_to_file(item)  #将爬取到的数据写入TXT文件
		write_to_DB(item)		#将爬取到的数据写入MySQL数据库

if __name__ == '__main__':
	for i in range(10):
		main(i*25)
	