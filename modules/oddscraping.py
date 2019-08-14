import sys
#Beatiful Soup - To parse the html
from bs4 import BeautifulSoup
import requests
#urllib.request - to make http request
import urllib.request
#To remove any language special characters
import unicodedata
# EMAIL library
import smtplib
#regular express library
import re
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from selenium import webdriver

from  datetime import datetime
from selenium.webdriver.chrome.options import Options

from time import sleep
import time

def fetch_odds(url):
	odds = []
	req1 = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
	r1 = urlopen(req1).read()
	soup = BeautifulSoup(r1, 'lxml')
	table = soup.find('div', id='oddetail')
	tourname = table.h1.text.strip()
	rows = table.select('tr')
	
	i = 0
	while i < len(rows):
		row = rows[i]
		home = row.select('td')[0].select('.matchname a:nth-of-type(1)')[0].text
		away = row.select('td')[0].select('.matchname a:nth-of-type(2)')[0].text

		cnt = i + 1
		while cnt < len(rows):
			rowd = rows[cnt]
			if rowd.has_attr('class') == False: #when it is new match item
				break
			if rowd.attrs['title'].find("Betclic") != -1:
				row_bc = cnt
			elif rowd.attrs['title'].find("Unibet") != -1:
				row_ub = cnt
			elif rowd.attrs['title'].find("Winamax") != -1:
				row_max = cnt
			cnt = cnt + 1
		row = rows[row_bc]		
		odd1 = float(row.select('td.bet')[0].text.strip())
		odd2 = float(row.select('td.bet')[1].text.strip())
		bcw = odd1
		bcl = odd2
		 
		row = rows[row_ub]
		odd1 = float(row.select('td.bet')[0].text.strip())
		odd2 = float(row.select('td.bet')[1].text.strip())
		ubw = odd1
		ubl = odd2
		
		row = rows[row_max]
		odd1 = float(row.select('td.bet')[0].text.strip())
		odd2 = float(row.select('td.bet')[1].text.strip())
		maxw = odd1
		maxl = odd2
		
		odd = {
			'home' : home,
			'away' : away,
			'bcw' : bcw,
			'bcl' : bcl,
			'ubw' : ubw,
			'ubl' : ubl,
			'maxw' : maxw,
			'maxl' : maxl,
			'tournament' : tourname, 
		}

		odds.append(odd)
		i = i + int(rows[i].td.attrs['rowspan'])
	return odds

def get_odds_data():
	start = time.time()
	url = "http://www.comparateur-de-cotes.fr/comparateur/tennis"
	req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
	r = urlopen(req).read()	
	print("it took" + str(time.time() - start) + "seconds to load data.")
	start = time.time()
	soup = BeautifulSoup(r, 'lxml')
	print("it took" + str(time.time() - start) + "seconds to parse data.")
	start = time.time()
	tennis_div = soup.find('div', class_="sportdiv", id="d2")
	divs = tennis_div.select('div.seperator')

	atpodds = []
	wtaodds = []

	for div in divs:
		temp_ele = div
		while True:
			temp_ele = temp_ele.nextSibling
			if temp_ele is None:
				break
			if temp_ele == '\n':
				continue
			if len(temp_ele.attrs) == 0 and temp_ele.name == 'div':
				title_div = temp_ele.find('div', class_='subhead')
				#Analyze the match title whether contains "ATP Tour"
				if title_div.text.find('ATP Tour') != -1:	
					lis = temp_ele.find_all('li')
					for li in lis:		
						href = li.find('a').attrs['href']
						if href.find('Doubles') != -1:
							continue
						suburl = href.split('/')[2]
						new_url = url + "/" + suburl
						odds = fetch_odds(new_url)
						atpodds = atpodds + odds
				elif title_div.text.find('WTA Tour') != -1:
					lis = temp_ele.find_all('li')
					for li in lis:
						href = li.find('a').attrs['href']
						if href.find('Doubles') != -1:
							continue
						suburl = href.split('/')[2]
						new_url = url + "/" + suburl
						odds = fetch_odds(new_url)
						wtaodds = wtaodds + odds
				else:
					continue
	result = {
		"atpodds" : atpodds,
		"wtaodds" : wtaodds,
	}

	print("it took" + str(time.time() - start) + "seconds to analyze the data.")
	return result

def get_bet365_odd():
	url = "https://www.bet365.com/"
	req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
	r = urlopen(req).read()
	soup = BeautifulSoup(r, 'lxml')
	return []
if __name__ == '__main__':
	#get_odds_data()
	get_bet365_odd()