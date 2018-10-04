from django.shortcuts import render
from django.http import HttpResponse
from .models import Searches, Campaigns
import requests
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

def index(request):
	if request.user.is_authenticated:
		return render(request, 'home/index.html',{
			'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'true',
			'showSignup' : 'false',
			'searchKey'  : ''
			})
	else :
		print (request.user.is_authenticated)
		return render(request, 'home/index.html',{
		'title': 'Demo App',
		'showLogin' : 'true',
		'showLogout' : 'false',
		'showSignup' : 'true',
		'searchKey'  : ' '
		})


def login(request):
	return render(request, 'home/login.html')

def search(request):
	search_list = []

	searchKey =request.GET.get('key' )
	flippaApiUrl = 'https://api.flippa.com/v3/listings?query=' + searchKey
	godaddyUrl = 'https://api.ote-godaddy.com/v1/domains/suggest?waitMs=1000&query=' + searchKey

	try:
		response = requests.get(flippaApiUrl)
		flippaSearchResultData = response.json()
		for ele in flippaSearchResultData['data']:
			if (ele['hostname'].find(searchKey) != -1 ):
				search_list.append({'domain' : ele['hostname'], 'api':'flippa'})
	except:
		print('flippa err')


	headers = { "accept": "application/json" , "Authorization": "sso-key UzQxLikm_46KxDFnbjN7cQjmw6wocia:46L26ydpkwMaKZV6uVdDWe"}
	try:
		response = requests.get(godaddyUrl, headers=headers)
		godaddySearchResultData = response.json()
		for ele in godaddySearchResultData:
			search_list.append({'domain' : ele['domain'], 'api':'godaddy'})	
	except:
		print('godaddy err')

	uid = request.user.id
	try:
		savedCampaigns = Campaigns.objects.filter(belongs_to = uid)
	except: 
		savedCampaigns = []

	if request.user.is_authenticated:
		return render(request, 'home/search.html',{
			'title': 'Demo App',
				'showLogin' : 'false',
				'showLogout' : 'true',
				'showSignup' : 'false',
				'saveSearch' : 'false',
				'searchKey'  : searchKey,
				'search_list' : search_list,
				'savedCampaigns': savedCampaigns
				})

	return render(request, 'home/search.html',{
		'title': 'Demo App',
			'showLogin' : 'true',
			'showLogout' : 'falaSe',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : searchKey,
			'search_list' : search_list,
			'savedCampaigns' : savedCampaigns
			})

def saveSearchKey(request):
	searchKey = request.GET.get('key')
	search = Searches(search_key = searchKey)
	search.save()
	savedSearckKeys =  Searches.objects.all()
	return render(request, 'home/profile.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'falaSe',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			'searchResultData' : savedSearckKeys
			})

def profile(request):
	savedSearckKeys =  Searches.objects.all()
	uid = request.user.id
	userobj = User.objects.get(id=uid)

	try:
		savedCampaigns = Campaigns.objects.filter(belongs_to = userobj)
	except: 
		savedCampaigns = []
	
	return render(request, 'home/profile.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'true',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			 'searchResultData' : savedSearckKeys,
			 'savedCampaigns'	: savedCampaigns
			})

def deleteKeyword(request):
	searchKeyId = request.GET.get('id')
	searchKey =  Searches.objects.get(id = searchKeyId)
	searchKey.delete()
	savedSearckKeys =  Searches.objects.all()
	return render(request, 'home/profile.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'false',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			'searchResultData' : savedSearckKeys,
			})

def newCampaign(request):
	return render(request, 'home/newCampaign.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'true',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			 'searchResultData' : ''
			})

def saveCampaign(request):
	campaignName =request.POST.get('campaignName' )
	campaignType =request.POST.get('campaignType' )
	campaignStart =request.POST.get('campaignStart' )
	campaignEnd =request.POST.get('campaignEnd' )

	uid = request.user.id
	userobj = User.objects.get(id=uid)

	newCampaign = Campaigns(name = campaignName , campaign_type= campaignType, start = campaignStart, end = campaignEnd , belongs_to = userobj)
	newCampaign.save()

	savedSearckKeys =  Searches.objects.all()

	uid = request.user.id
	try:
		savedCampaigns = Campaigns.objects.get(belongs_to = uid)
	except: 
		savedCampaigns = []

	return HttpResponseRedirect("/profile")


def campaignOverview(request):

	uid = request.user.id
	userobj = User.objects.get(id=uid)

	try:
		savedCampaigns = Campaigns.objects.filter(belongs_to = userobj)
	except: 
		savedCampaigns = []
	return render(request, 'home/campaignOverview.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'false',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			'savedCampaigns'	: savedCampaigns
			})

def deleteCampaign(request):
	searchKeyId = request.GET.get('id')
	print(searchKeyId)
	searchKey =  Campaigns.objects.get(id = searchKeyId)
	searchKey.delete()
	
	try:
		savedCampaigns = Campaigns.objects.get(belongs_to = uid)
	except: 
		savedCampaigns = []
	return HttpResponseRedirect("/campaignOverview")



def saveToCampaign(request):
	searchKey = request.POST.get('searchKey')
	campaignId = request.POST.get('campaign')
	if campaignId :
		campaignInstance =  Campaigns.objects.get(id = campaignId)
		search = Searches(search_key = searchKey, campaign_id = campaignInstance)
		search.save()
		savedSearckKeys =  Searches.objects.all()
		return HttpResponseRedirect("/profile")
	else:
		return HttpResponseRedirect("/")	
	


def newUser(request):
	return render(request, 'home/signup.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'false',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			})

def saveNewUser(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	email = request.POST.get('email')

	user = User.objects.create_user(username=username, email=email, password=password)

	return HttpResponseRedirect("/")