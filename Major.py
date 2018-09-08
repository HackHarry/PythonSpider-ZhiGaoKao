import requests
import time
import os
import csv
from pyquery import PyQuery as pq

number = 100
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,z;q=0.8'
    }
	
def get_majors(ID):
	url = 'http://www.zhigaokao.cn/majored/getCategoryMajoredList.do?'
	payload = {
			'userKey': 'www',
			'req': 'ajax',
			'categoryId': ID
		}
	response = requests.get(url, headers=headers, params=payload)
	items = response.json().get('bizData')
	return(items)

def bulid(items):
	path = '.\\majors\\' + items.get('name') + '\\'
	item = items.get('childList')
	for its in item:
		pa = path + its.get('name')
		isExists=os.path.exists(pa)
		if not isExists:
			os.makedirs(pa)
		it = its.get('childList')
		for i in it:
			p = pa + '\\' + i.get('name') + '.csv'
			with open(p, 'w') as csvfile:
				writer = csv.writer(csvfile, lineterminator='\n')
				results = get_data(i.get('id'))
				for result in results:
					writer.writerow([result.get('name'), result.get('province'), result.get('property')])
				print(p + 'finish!')
				

def get_data(ID):
	url = 'http://www.zhigaokao.cn/majored/getMajorOpenUniversityList.do?'
	payload = {
			'userKey': 'www',
			'req': 'ajax',
			'majoredId': ID,
			'majorType': 1,
			'offset': 0,
			'row': 10
		}
	results = []
	length = 10
	while (payload['offset'] < number) and (length == 10):
		response = requests.get(url, headers=headers, params=payload)
		items = response.json().get('bizData').get('universityList')
		length = len(items)
		for item in items:
			results.append(item)
		payload['offset'] = payload['offset'] + length
		time.sleep(1)
		print(ID, payload['offset'])
	return(results)

def main():
	for i in range(13):
		if i == 10: 
			contiune
		bulid(get_majors(i+1))

if __name__ == '__main__' :
	main()
