from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django.urls import reverse_lazy

from .models import ATPPlayer
from .models import WTAPlayer
from modules import webscrapping

class ATPPlayerCreateView(CreateView):
	model = ATPPlayer
	fields = '__all__'
	template_name = "player/player_form.html"
	success_url = reverse_lazy('player:player_list')

class ATPPlayerUpdateView(UpdateView):
	model = ATPPlayer
	fields = '__all__'
	template_name = "player/player_form.html"
	success_url = reverse_lazy('player:player_list')

class ATPPlayerDeleteView(DeleteView):
	model = ATPPlayer
	fields = '__all__'
	template_name = "player/player_delete_confirm.html"
	success_url = reverse_lazy('player:player_list')

def atp_player_list(request, template_name='player/player_list.html'):
	players = webscrapping.get_atp_players()
	
	plys = ATPPlayer.objects.all()

	for pl in plys:
		pl.nicknames = ""
		pl.save()

	for player in players:
		try: 
			old_players = ATPPlayer.objects.filter(name = player['name'])
			if len(old_players) > 0:
				old_p = old_players[0]
				old_p.rank = player['rank']	
				old_p.max_rank = player['max_rank']
				old_p.country = player['country']
				old_p.age = player['age']
				old_p.pts = player['pts']
				old_p.inc_pts = player['inc_pts']
				old_p.dec_pts = player['dec_pts']
				old_p.cur_tournament = player['cur_tournament']
				old_p.prev_tournament = player['prev_tournament']
				old_p.next_pts = player['next_pts']
				old_p.max_pts = player['max_pts']
				#adding the nickname
				if old_p.nicknames.find(player['origin_name']) == -1:
					old_p.nicknames += "#" + player['origin_name']
				if old_p.nicknames.find(player['name']) == -1:
					old_p.nicknames += "#" + player['name']
				old_p.save()
				continue
		except:
			print(player['name'])
		new_p = ATPPlayer()
		new_p.rank = player['rank']
		new_p.max_rank = player['max_rank']
		new_p.name = player['name']
		new_p.country = player['country']
		new_p.age = player['age']
		new_p.pts = player['pts']
		new_p.inc_pts = player['inc_pts']
		new_p.dec_pts = player['dec_pts']
		new_p.cur_tournament = player['cur_tournament']
		new_p.prev_tournament = player['prev_tournament']
		new_p.next_pts = player['next_pts']
		new_p.max_pts = player['max_pts']
		new_p.nicknames = '#' + player['name'] + '#' + player['origin_name']  
		new_p.save()

	data = {
		'player_list' : players,
	}

	# pxscores = webscrapping.get_atp_players_xscores()
	# for x in range(0, 100):
	# 	p = pxscores[x]
	# 	try:
	# 		players = ATPPlayer.objects.filter(nicknames__contains=p)
	# 		if len(players) == 0:
	# 			print(p + str(x))
	# 	except:
	# 		print(p + str(x))
	return render(request, template_name, data)

def wta_player_list(request, template_name='player/player_list.html'):
	players = webscrapping.get_wta_players()
	for player in players:
		try: 
			old_players = WTAPlayer.objects.filter(name = player['name'])
			if len(old_players) > 0:
				old_p = old_players[0]
				old_p.rank = player['rank']	
				old_p.max_rank = player['max_rank']
				old_p.country = player['country']
				old_p.age = player['age']
				old_p.pts = player['pts']
				old_p.inc_pts = player['inc_pts']
				old_p.dec_pts = player['dec_pts']
				old_p.cur_tournament = player['cur_tournament']
				old_p.prev_tournament = player['prev_tournament']
				old_p.next_pts = player['next_pts']
				old_p.max_pts = player['max_pts']
				#adding the nickname
				if old_p.nicknames.find(player['origin_name']) == -1:
					old_p.nicknames += "#" + player['origin_name']
				if old_p.nicknames.find(player['name']) == -1:
					old_p.nicknames += "#" + player['name']
				old_p.save()
				continue
		except:
			print(player['name'])
		new_p = WTAPlayer()
		new_p.rank = player['rank']
		new_p.max_rank = player['max_rank']
		new_p.name = player['name']
		new_p.country = player['country']
		new_p.age = player['age']
		new_p.pts = player['pts']
		new_p.inc_pts = player['inc_pts']
		new_p.dec_pts = player['dec_pts']
		new_p.cur_tournament = player['cur_tournament']
		new_p.prev_tournament = player['prev_tournament']
		new_p.next_pts = player['next_pts']
		new_p.max_pts = player['max_pts']
		new_p.nicknames = '#' + player['name'] + '#' + player['origin_name']  
		new_p.save()
	
	data = {
		'player_list' : players,
	}
	# pxscores = webscrapping.get_wta_players_xscores()
	# for x in range(0, 100):
	# 	p = pxscores[x]
	# 	try:
	# 		players = WTAPlayer.objects.filter(nicknames__contains=p)
	# 		if len(players) == 0:
	# 			print(p + str(x))
	# 	except:
	# 		print(p + str(x))
	return render(request, template_name, data)
# def player_list(request, template_name='player/player_list.html'):
# 	players = Player.objects.all()
# 	data = {
# 		'player_list' : players, 
# 	}
# 	return render(request, template_name, data)

# def player_create(request, template_name='player/player_create.html'):
# 	form = PlayerForm
# 	if form.is_valid == True:
# 		form.save()
# 		return redirect('player:player_list')

def find_difference():

	return
def player_index(request):
	return HttpResponse('<h1> Welcome to our players page </h1>')

def about_page(request):
	return HttpResponse('<h1> Welcome to our about page </h1>')

def contact_page(request):
	return HttpResponse('<h1> Welcome to our contact page </h1>')

