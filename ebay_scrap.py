import bs4 as bs
import urllib.request
import csv

def get_page(url):
	try:
		source = urllib.request.urlopen(url).read()
		soup = bs.BeautifulSoup(source, 'lxml')
		return soup
	except:
		print("server Error")	

def get_details(soup):
	try:
		title = soup.find('h1', id ='itemTitle').text 	
	except:
		title = ''	

	try:
		try:
			price = soup.find('span', id = 'prcIsum').text.strip().split()
			currency , amount = price
		except:
			amount = 'on bid'
			currency = 'US'
			
	except:
		amount = ''
		currency = ''

	

	try:
		link = soup.find('a', class_ = 'vi-txt-underline').text.strip().replace('\xa0','')
	except:
		link = '0 sold'

	data = {
		'Title':title,
		'Price':amount,
		'Currency':currency,
		'Items_Sold':link
	}	

	return data


def get_url_data(soup):
	try:
		links = soup.find_all('a', class_='s-item__link')
	except:	
		links - []

	urls = [item.get('href') for item in links]
	
	return urls	

def transfer(data,link):
	with open('Data.csv','a') as csvfile:
		writer = csv.writer(csvfile)

		row = [data['Title'],data['Price'],data['Currency'],data['Items_Sold'],link]

		writer.writerow(row)

def main(det):

	url = f'https://www.ebay.com/sch/i.html?_nkw={det}&_pgn=1'
	products = get_url_data(get_page(url))

	for product in products:
		data = get_details(get_page(product))
		transfer(data,product)
	print('Data Transfered')	



detail = input("Enter Product to be searched on EBAY: ").split()
det = ''.join(detail)
main(det)