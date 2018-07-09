import requests
import re
from requests.exceptions import RequestException
from flask import json

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    pattern1 = re.compile('<li>.*?="clearfix">.*?="mh-item-detali">.*?href="(.*?)"'
                          +'.*?title="(.*?)">.*?"color:#666;">(.*?)</a>.*?class="desc">\s+(.*?)\s+</div>', re.S)
    pattern2 = re.compile('="mh-itme-top">.*?="mh-item-tip-detali">.*?href="(.*?)"'
                          +'.*?title="(.*?)">.*?="_blank">(.*?)</a>.*?class="desc">\s+(.*?)\s+</div>', re.S)
    items1=re.findall(pattern1,html)
    items2=re.findall(pattern2,html)
    for item1 in items1:
        yield{
            'image': 'http://www.1kkk.com'+item1[0],
            'title': item1[1],
            'author': item1[2],
            'topic': item1[3]
        }
    for item2 in items2:
        yield{
            'image': 'http://www.1kkk.com'+item2[0],
            'title': item2[1],
            'author': item2[2],
            'topic': item2[3]
        }


def write_to_file(content):
    with open('manhua.txt','a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False)+'\n')
        f.close()

def main():
    url='http://www.1kkk.com/manhua-rank/'
    html=get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)
    #print(html)


if __name__=='__main__':
    main()