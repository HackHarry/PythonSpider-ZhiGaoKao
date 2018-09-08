import requests
import time
import csv
from pyquery import PyQuery as pq

number = 100
headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,z;q=0.8'
    }

def get_id():
	url = 'http://www.zhigaokao.cn/university/getRemoteProvinceList.do?'
	payload = {
			'userKey': 'www',
			'req': 'ajax',
		}
	response = requests.get(url, headers=headers, params=payload)
	items = response.json().get('bizData')
	IDs = []
	for item in items:
		IDs.append(item.get('id'))
	return IDs

def get_data(ID):
	url = 'http://www.zhigaokao.cn/university/getRemoteUniversityList.do?'
	payload = {
			'userKey': 'www',
			'req': 'ajax',
			'areaid': ID,
			'educationLevel': 1,
			'offset': 0,
			'rows': 10
		}
	results = []
	length = 10
	while (payload['offset'] < number) and (length == 10):
		response = requests.get(url, headers=headers, params=payload)
		items = response.json().get('bizData').get('universityList')
		length = len(items)
		payload['offset'] = payload['offset'] + length
		for item in items:
			results.append(item)
		time.sleep(1)
		print(payload['offset'])
	print_csv(results)

def print_csv(results):
	path = '.\province\\' + results[0].get('province') + '.csv'
	with open(path, 'w') as csvfile:
		writer = csv.writer(csvfile, lineterminator='\n')
		for result in results:
			writer.writerow([result.get('name'), result.get('property')])
		print(path + ' finish!')

def main():
	IDs = get_id()
	for ID in IDs:
		get_data(ID)

if __name__ == '__main__' :
	main()
