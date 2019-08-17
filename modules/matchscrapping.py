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
from  datetime import datetime
from time import sleep

WINDOW_SIZE = "1920,1080"
CHROME_PATH = "c:/chromedriver/chromedriver.exe"

def fetch_xcore_data(soup, type):
	matches = []
	if type == 1:
		elements = soup.find_all('div', class_='match_line', attrs={'data-country-name' : 'ATP-S'})
	else:	
		elements = soup.find_all('div', class_='match_line', attrs={'data-country-name' : 'WTA-S'})
	for ele in elements:
		tour_arrs = ele.attrs['data-league-name'].split(' ')
		tournament_name = tour_arrs[0]
		location = tour_arrs[1]
		time_str = ele.attrs['data-ko']
		date_str = ele.attrs['data-matchday']
		date = datetime.strptime(date_str + ' ' + time_str, '%Y-%m-%d %H:%M')
		round = ele.attrs['data-league-round']
		str = ele.attrs['data-home-team']
		try:
			_id = str.index('(')
			p1_name = str[:_id-1]
		except:
			p1_name = str

		str = ele.find('div', class_='score_away_txt').span.text.strip()
		try:
			_id = str.index('(')
			p2_name = str[:_id-1]
		except:
			p2_name = str

		match_status = ele.attrs['data-statustype']
		if  match_status == 'sched':
			new_match = {
				'date' : date,
				'round' : round,
				'tournament' : tournament_name,
				'status' : match_status,
				'comment' : match_status,
				'home' : p1_name,
				'away' : p2_name,
				'winner' : '',
				'loser' : '',
				'home_r1' : -1,
				'away_r1' : -1,
				'home_r2' : -1,
				'away_r2' : -1,
				'home_r3' : -1,
				'away_r3' : -1,
				'home_r4' : -1,
				'away_r4' : -1,
				'home_r5' : -1,
				'away_r5' : -1,
				'home_winsets' : -1,
				'away_winsets' : -1,
				'totalsets' : -1,
				'totalgames' : -1,
				'bestof' : 3,
				'home' : p1_name, 
				'away' : p2_name,
			}
			matches.append(new_match)
			continue

		divset = ele.find_all('div', class_='score_ft score_cell centerTXT')[0]
		if divset.find_all('div')[0].text != '-':	
			p1_won_sets = int(divset.find_all('div')[0].next, 10)
			p2_won_sets = int(divset.find_all('div')[1].next, 10)
		else:
			p1_won_sets = -1
			p2_won_sets = -1
		total_sets = p1_won_sets + p2_won_sets
		winner = ""
		loser = ""

		divsets = ele.find_all('div', class_='score_ht score_cell centerTXT')

		totalgames = 0
		#set1
		score_div1  = divsets[0]
		if score_div1.find_all('div')[0].text != '-':	
			home_r1 = int(score_div1.find_all('div')[0].next, 10)
			away_r1 = int(score_div1.find_all('div')[1].next, 10)
			totalgames += home_r1 + away_r1
		else:
			home_r1 = -1
			away_r1 = -1
		
		#set2
		score_div2  = divsets[1]
		if score_div2.find_all('div')[0].text != '-':	
			home_r2 = int(score_div2.find_all('div')[0].next, 10)
			away_r2 = int(score_div2.find_all('div')[1].next, 10)
			totalgames += home_r2 + away_r2
		else:
			home_r2 = -1
			away_r2 = -1

		#set3
		score_div3  = divsets[2]
		if score_div3.find_all('div')[0].text != '-':	
			home_r3 = int(score_div3.find_all('div')[0].next, 10)
			away_r3 = int(score_div3.find_all('div')[1].next, 10)
			totalgames += home_r3 + away_r3
		else: 
			home_r3 = -1
			away_r3 = -1

		#set4
		score_div4  = divsets[3]
		if score_div4.find_all('div')[0].text != '-':	
			home_r4 = int(score_div4.find_all('div')[0].next, 10)
			away_r4 = int(score_div4.find_all('div')[1].next, 10)
			totalgames += home_r4 + away_r4
		else: 
			home_r4 = -1
			away_r4 = -1

		#set5
		score_div5  = divsets[4]
		if score_div5.find_all('div')[0].text != '-':	
			home_r5 = int(score_div5.find_all('div')[0].next, 10)
			away_r5 = int(score_div5.find_all('div')[1].next, 10)
			totalgames += home_r5 + away_r5
		else: 
			home_r5 = -1
			away_r5 = -1
				
		if p1_won_sets > p2_won_sets:
			winner = p1_name
			loser = p2_name
		else:
			winner = p2_name
			loser = p1_name
			
		new_match = {
			'date' : date,
			'round' : round,
			'tournament' : tournament_name,
			'location' : location,
			'status' : match_status,
			'comment' : match_status,
			'winner' : winner,
			'loser' : loser,
			'home_r1' : home_r1,
			'away_r1' : away_r1,
			'home_r2' : home_r2,
			'away_r2' : away_r2,
			'home_r3' : home_r3,
			'away_r3' : away_r3,
			'home_r4' : home_r4,
			'away_r4' : away_r4,
			'home_r5' : home_r5,
			'away_r5' : away_r5,
			'home_winsets' : p1_won_sets,
			'away_winsets' : p2_won_sets,
			'totalsets' : p1_won_sets + p1_won_sets,
			'totalgames' : totalgames,
			'bestof' : 3,
			'home' : p1_name, 
			'away' : p2_name,
		}
		matches.append(new_match)

	return matches

def get_atp_matches_from_xscores():
	url = "https://www.xscores.com/tennis/"
	req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
	r = urlopen(req).read()
	soup = BeautifulSoup(r, 'lxml')
	
	# prev_url = soup.find(class_="dateLeftArrow", attrs={'title':'Previous Day'}).a.attrs['href']
	# prev_day_url = urljoin(url, prev_url)
	# prev_r = urlopen(Request(prev_day_url, headers={'User-Agent' : 'Mozilla/5.0'})).read()
	# prev_soup = BeautifulSoup(prev_r, 'lxml')

	# next_url = soup.find(class_="dateRightArrow", attrs={'title':'Next Day'}).a.attrs['href']
	# next_day_url = urljoin(url, next_url)
	# next_r = urlopen(Request(next_day_url, headers={'User-Agent' : 'Mozilla/5.0'})).read()
	# next_soup = BeautifulSoup(next_r, 'lxml')

	today_matches = fetch_xcore_data(soup, 1)
	# prev_matches = fetch_xcore_data(prev_soup, 1)
	# next_matches = fetch_xcore_data(next_soup, 1)
	# matches_ = prev_matches + today_matches + next_matches
	return today_matches

def get_wta_matches_from_xscores():
	url = "https://www.xscores.com/tennis/"
	req = Request(url, headers={'User-Agent' : 'Mozilla/5.0'})
	r = urlopen(req).read()
	soup = BeautifulSoup(r, 'lxml')
	
	prev_url = soup.find(class_="dateLeftArrow", attrs={'title':'Previous Day'}).a.attrs['href']
	prev_day_url = urljoin(url, prev_url)
	prev_r = urlopen(Request(prev_day_url, headers={'User-Agent' : 'Mozilla/5.0'})).read()
	prev_soup = BeautifulSoup(prev_r, 'lxml')

	next_url = soup.find(class_="dateRightArrow", attrs={'title':'Next Day'}).a.attrs['href']
	next_day_url = urljoin(url, next_url)
	next_r = urlopen(Request(next_day_url, headers={'User-Agent' : 'Mozilla/5.0'})).read()
	next_soup = BeautifulSoup(next_r, 'lxml')

	today_matches = fetch_xcore_data(soup, 2)
	prev_matches = fetch_xcore_data(prev_soup, 2)
	next_matches = fetch_xcore_data(next_soup, 2)
	matches_ = prev_matches + today_matches + next_matches
	return matches_


def get_match_detail_from_url(soup):

	# _options = Options()  
	# _options.add_argument("--headless")  
	# _options.add_argument("--window-size=%s" % WINDOW_SIZE)
	# _options.add_argument('--no-sandbox')
	# _options.add_argument('--disable-dev-shm-usage')
	# _options.binary_location = CHROME_PATH

	# browser = webdriver.Chrome(executable_path=CHROME_PATH, chrome_options=_options)
	# browser.get(url)
	# soup = BeautifulSoup(browser.page_source, 'lxml')

	divs = soup.find_all('div', 'statRow')

	if len(divs) == 0:
		return None
	
	#Player 1 aces
	str = divs[0].find('div','statText statText--homeValue').text.strip()
	p1_aces = int(str, 10)

	#Player 2 aces
	str = divs[0].find('div','statText statText--awayValue').text.strip()
	p2_aces = int(str, 10)

	#Player 1 % double faults
	str = divs[1].find('div','statText statText--homeValue').text.strip()
	p1_double_fault = int(str, 10)

	#Player 2 % double faults
	str = divs[1].find('div','statText statText--awayValue').text.strip()
	p2_double_fault = int(str, 10)

	#Player 1 % 1st serve points won
	str = divs[3].find('div','statText statText--homeValue').text.strip()
	str_percent = str[:str.index('%')]
	p1_ser1_pts = int(str_percent, 10)

	#Player 2 % 1st serve points won
	str = divs[3].find('div','statText statText--awayValue').text.strip()
	str_percent = str[:str.index('%')]
	p2_ser1_pts = int(str_percent, 10)

	#Player 1 % 2nd serve points won
	str = divs[4].find('div','statText statText--homeValue').text.strip()
	str_percent = str[:str.index('%')]
	p1_ser2_pts = int(str_percent, 10) 

	#Player 2 % 2nd serve points won
	str = divs[4].find('div','statText statText--awayValue').text.strip()
	str_percent = str[:str.index('%')]
	p2_ser2_pts = int(str_percent, 10)

	#Player 1 % serve points won
	str = divs[10].find('div','statText statText--homeValue').text.strip()
	str_percent = str[:str.index('%')]
	p1_ser_pts = int(str_percent, 10) 

	#Player 2 % serve points won
	str = divs[10].find('div','statText statText--awayValue').text.strip()
	str_percent = str[:str.index('%')]
	p2_ser_pts = int(str_percent, 10)

	
	#Player 1 % receive points won
	str = divs[11].find('div','statText statText--homeValue').text.strip()
	str_percent = str[:str.index('%')]
	p1_rec_pts = int(str_percent, 10) 

	#Player 2 % receive points won
	str = divs[11].find('div','statText statText--awayValue').text.strip()
	str_percent = str[:str.index('%')]
	p2_rec_pts = int(str_percent, 10)

	#Player 1 % total points earned
	str = divs[12].find('div','statText statText--homeValue').text.strip()
	str_percent = str[:str.index('%')]
	p1_total_pts = int(str_percent, 10) 
	
	#Player 2 % total points earned
	str = divs[12].find('div','statText statText--awayValue').text.strip()
	str_percent = str[:str.index('%')]
	p2_total_pts = int(str_percent, 10)

	if p1_total_pts > p2_total_pts:
		waces = p1_aces
		wdfault = p1_double_fault
		wser1 = p1_ser1_pts
		wser2 = p1_ser2_pts
		wser = p1_ser_pts
		wrec = p1_rec_pts
		wtotal = p1_total_pts
		laces = p2_aces
		ldfault = p2_double_fault
		lser1 = p2_ser1_pts
		lser2 = p2_ser2_pts
		lser = p2_ser_pts
		lrec = p2_rec_pts
		ltotal = p2_total_pts
	else:
		waces = p2_aces
		wdfault = p2_double_fault
		wser1 = p2_ser1_pts
		wser2 = p2_ser2_pts
		wser = p2_ser_pts
		wrec = p2_rec_pts
		wtotal = p2_total_pts
		laces = p1_aces
		ldfault = p1_double_fault
		lser1 = p1_ser1_pts
		lser2 = p1_ser2_pts
		lser = p1_ser_pts
		lrec = p1_rec_pts
		ltotal = p1_total_pts

	detail = {
		'waces' 		: waces,
		'wdfault' 		: wdfault, 
		'wser1' 		: wser1,
		'wser2' 		: wser2,
		'wser' 			: wser,
		'wrec' 			: wrec,
		'wtotal' 		: wtotal,
		'laces' 		: laces,
		'ldfault' 		: ldfault, 
		'lser1' 		: lser1,
		'lser2' 		: lser2,
		'lser' 			: lser,
		'lrec' 			: lrec,
		'ltotal'		: ltotal,
		'home' 			: '',
		'away' 			: '',
		'home_country' 	: '',
		'away_country' 	: '',
		'date' 			: None,
		'tournament'	: '',
	}
	return detail

#get performance data
def get_atp_match_from_flashresultat():
	url = "https://www.flashresultats.fr/tennis/"

	#options for not displaying the chrome browser
	_options = Options()  
	_options.add_argument("--headless")  
	_options.add_argument("--window-size=%s" % WINDOW_SIZE)
	_options.add_argument('--no-sandbox')
	_options.add_argument('--disable-dev-shm-usage')

	browser = webdriver.Chrome(chrome_options=_options)
	browser.get(url)
	sleep(5)
	#navigate to the previous day
	prev_div = browser.find_element_by_css_selector('div.calendar__direction.calendar__direction--yesterday')
	prev_div.click()
	sleep(3)
	soup = BeautifulSoup(browser.page_source, 'lxml')
	header_divs = soup.find_all('div', class_="event__header")
	
	details = [] # match details
	div_datepicker = soup.find('div', class_="calendar__datepicker")
	str = div_datepicker.text.strip()
	day = int(str[:2], 10)
	month = int(str[3:5], 10)
	year = datetime.now().year

	date = datetime.now()
	date.replace(year=year,month=month, day=day)
		
	for hdiv in header_divs:
		tour_type = hdiv.find('span', class_= 'event__title--type')
		if tour_type.text != 'ATP - SIMPLES':
			continue
		tour_div = hdiv.nextSibling
		while True:
			if tour_div.attrs['id'][0:3] != 'g_2':
				break
			tour_id_str = tour_div.attrs['id'][4:]
			url = "https://www.flashresultats.fr/match/" + tour_id_str + "/#statistiques-du-match;0"
			browser.get(url)
			sleep(5)
			dsoup = BeautifulSoup(browser.page_source, 'lxml')
			detail = get_match_detail_from_url(dsoup)
			if detail == None:
				tour_div = tour_div.nextSibling
				tour_div_cls_arr = tour_div.attrs['class']
				if "event__match" not in tour_div_cls_arr:
					break
				continue
			#Get the name, country of player1 and player2
			home_str = tour_div.find('div', class_="event__participant--home").text.strip()
			home_name = home_str[: home_str.index('(')-1]
			home_country = home_str[home_str.index('(')+1: home_str.index(')')]			
			away_str = tour_div.find('div', class_="event__participant--away").text.strip()
			away_name = away_str[: away_str.index('(')-1]
			away_country = away_str[away_str.index('(')+1: away_str.index(')')]

			detail['home'] = home_name
			detail['home_country'] = home_country
			detail['away'] = away_name
			detail['away_country'] = away_country
			print(detail)
			details.append(detail)

			#check if next sibling is atp match
			tour_div = tour_div.nextSibling
			tour_div_cls_arr = tour_div.attrs['class']
			if "event__match" not in tour_div_cls_arr:
				break
	browser.quit()
	return details

if __name__ == '__main__':
	get_atp_matches_from_xscores()
	# get_atp_match_from_flashresultat()