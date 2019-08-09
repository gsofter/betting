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


#extract the matches data from the soup
def fetch_matches(soup):
	items = soup.find_all('div', id=True, attrs={'class' : re.compile("match_line")})
	print(items)

def get_atp_players_xscores():
	r = urllib.request.urlopen('https://www.xscores.com/tennis/rankings/atp-s/top-100').read()
	soup = BeautifulSoup(r, 'lxml')
	players = []
	elements = soup.find_all('div', class_="score_row")
	for ele in elements:
		txt = ele.find_all('div')[3].text.strip()
		name = txt[:txt.index('(')-1]
		players.append(name)
	return players

def get_wta_players_xscores():
	r = urllib.request.urlopen('https://www.xscores.com/tennis/rankings/wta-s/top-100').read()
	soup = BeautifulSoup(r, 'lxml')
	players = []
	elements = soup.find_all('div', class_="score_row")
	for ele in elements:
		txt = ele.find_all('div')[3].text.strip()
		name = txt[:txt.index('(')-1]
		players.append(name)
	return players


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
		if ch == 'Í' or ch == 'Î' or ch == 'Ì' or ch == 'Ï' or ch == 'İ':
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
def fetch_players(soup):
	players_ = []
	players_table = soup.find('table', id="u868"); #player table element 
	elements = players_table.tbody.find_all('tr',  {'bgcolor' : ['white', '#E7E7E7']})

	for ele in elements:
		tds = ele.find_all('td')
		rank = tds[0].text.strip()
		rank = int(rank, 10)

		tds_b = tds[1].find_all('b')
		max_rank_text = tds_b[1].text.strip()
		max_rank = 0
		if max_rank_text == 'CH':
			max_rank = 0
		elif max_rank_text.find('NCH') != -1:
			max_rank = -1
		else :
			max_rank= int(max_rank_text, 10)
		
		origin_name = tds[3].text.strip()
		name = get_formatted_name(origin_name)
		country = ele.attrs['class'][0]
		age = int(tds[4].next, 10)
		pts_str = tds[6].text.strip()
		pts = int(pts_str, 10)
		inc_pts_str = tds[7].text.strip()
		inc_pts = get_pts_int(inc_pts_str)
		dec_pts_str = tds[8].text.strip()
		dec_pts = get_pts_int(dec_pts_str)
		cur_tournament = tds[9].text.strip()
		prev_tournament = tds[10].text.strip()

		next_pts_str = tds[12].text.strip()
		next_pts = get_pts_int(next_pts_str)
		max_pts_str = tds[13].text.strip()
		max_pts = get_pts_int(max_pts_str)

		new_player = {
			'rank'    : rank,
			'max_rank'    : max_rank,
			'name' 	  : name,
			'country' : country,
			'age'	: age,
			'pts'   : pts,
			'inc_pts' : inc_pts,
			'dec_pts' : dec_pts,
			'cur_tournament' : cur_tournament,
			'prev_tournament' : prev_tournament,
			'next_pts' : next_pts,
			'max_pts'	: max_pts,
			'origin_name' : origin_name,
		}
		players_.append(new_player)
	return players_

def get_atp_players():
	url = "https://live-tennis.eu/en/atp-live-ranking"
	req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
	r = urlopen(req).read()
	soup = BeautifulSoup(r, 'lxml')
	players_ = fetch_players(soup)
	return players_

def get_wta_players():
	url = "https://live-tennis.eu/en/wta-live-ranking"
	req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
	r = urlopen(req).read()		
	soup = BeautifulSoup(r, 'lxml')
	players_ = fetch_players(soup)
	return players_

if __name__ == '__main__':
	#get_wta_players()
	get_atp_players_xscores()