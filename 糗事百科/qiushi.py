import requests
import re

def main(offset):
	url='https://www.qiushibaike.com/8hr/page/'+str(offset+1)+'/'
	html=requests.get(url).text
	pattern=re.compile('class="content">.*?<span>(.*?)</span>',re.S)
	item=re.findall(pattern, html)
	for i in item:
		print(i)
		print('----------')

if __name__ == '__main__':
	for x in range(13):
		main(x)
	