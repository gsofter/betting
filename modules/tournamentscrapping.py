#Beatiful Soup - To parse the html
from bs4 import BeautifulSoup
#urllib.request - to make http request
import urllib.request
#To remove any language special characters
import unicodedata
# EMAIL library
import smtplib
#regular express library
import re

from datetime import datetime


from urllib.request import Request, urlopen


#Function to convert special characters from a text to standard text

def remove_uknown_characters(input_str):
	nfkd_form = unicodedata.normalize('NFKD', input_str)
	only_ascii = nfkd_form.encode('ASCII', 'ignore')
	return only_ascii.decode()

def filter_duplicates(news_list):
	return_list = []
	for item in news_list:
		if(item not in return_list):
			return_list.append(item)
	return return_list

def get_formatted_name(str):
	pos = str.index(' ')
	surname = str[:pos-1]
	familyname = str[pos+1:]
	tstr = familyname + ' ' + surname[0] + '.'
	tstr = tstr.upper()
	result = ''
	for x in range(0, len(tstr)):
		ch = tstr[x]
		if ch == 'Á' or ch == 'Â' or ch == 'À' or ch == 'Å' or ch == 'Ã' or ch == 'Ä' or ch == 'Ă':
			ch = 'A'
		if ch == 'Ç' or ch == 'Ć' or  ch == 'Č':
			ch = 'C'
		if ch == 'É' or ch == 'Ê' or ch == 'È' or ch == 'Ë' or ch == 'Ē' or ch == 'Ę':
			ch = 'E'
		if ch == 'Í' or ch == 'Î' or ch == 'Ì' or ch == 'Ï':
			ch = 'I'
		if ch == 'Ñ' or ch == 'Ń':
			ch = 'N'
		if ch == 'Ó' or ch == 'Ô' or ch == 'Ò' or ch == 'Ø' or ch == 'Õ' or ch == 'Ö':
			ch = 'O'
		if ch == 'Š' or ch == 'Ś' or ch == 'Ș':
			ch = 'S'
		if ch == 'Ř':
			ch = 'R'
		if ch == 'Ð':			
			ch = 'D'
		if ch == 'Ú' or ch == 'Ü' or ch == 'Ů':
			ch = 'U'
		if ch == 'Ý':
			ch = 'Y'
		if ch == 'Ž' or ch == 'Ż':
			ch = 'Z'
		result += ch
	return result

def get_pts_int(str):
	result = 0
	if str == '-':
		result = 0
	else:
		result = int(str, 10)
	return result

#extract the players data from the soup
def fetch_tournaments(soup):
	tournaments_ = []
	elements = soup.find_all('div',  {'class' : ['score_row tennis_row e_true', 'score_row tennis_row o_true']})
	for ele in elements:
		divs = ele.find_all('div')
		date_str = divs[0].getText()
		date = datetime.strptime(date_str, '%d-%m-%Y').date()
		name = divs[1].text.strip()
		location = divs[2].text.strip()
		series = divs[4].text.strip()
		surface = divs[5].text.strip()
		price = divs[6].text.strip()
		#_price = price_str.replace('.', '').replace('$', '')
		#price = int(_price, 10)
		round_str = divs[7].text.strip()
		round = ''
		try: 
			_id = round_str.index('-')
			round = round_str[:_id]
		except:
			round = round_str
		
		new_tour = {
			'round' : round,
			'date' : date,
			'name' : name,
			'location' : location,
			'series' : series,
			'surface' : surface,
			'price' : price
		}

		tournaments_.append(new_tour)

	return tournaments_

def get_atp_tournaments():
	url = "https://www.xscores.com/tennis/tournaments/atp-tour/2019"
	req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
	r = urlopen(req).read()	
	soup = BeautifulSoup(r, 'lxml')
	tournaments_ = fetch_tournaments(soup)
	return tournaments_

def get_wta_tournaments():
	url = "https://www.xscores.com/tennis/tournaments/wta-tour/2019"
	req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
	r = urlopen(req).read()	
	soup = BeautifulSoup(r, 'lxml')
	tournaments_ = fetch_tournaments(soup)
	return tournaments_
	
if __name__ == '__main__':
	get_atp_tournaments()