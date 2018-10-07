from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Searches, Campaigns, SearchResults
import requests
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
	search_list = makeSearchAPICall(searchKey)

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

def makeSearchAPICall(key):
	search_list = []
	searchKey = key
	flippaApiUrl = 'https://api.flippa.com/v3/listings?query=' + searchKey
	godaddyAPIUrl = 'https://api.ote-godaddy.com/v1/domains/suggest?waitMs=1000&query=' + searchKey
	godaddyUrl = 'https://find.godaddy.com/domainsapi/v1/search/spins?pagestart=0&pagesize=60&key=dpp_search&q='+searchKey+'&tlds=&source=&maxsld=&pc=&ptl='

	response = requests.get(flippaApiUrl)
	flippaSearchResultData = response.json()
	for ele in flippaSearchResultData['data']:
		if (ele['hostname'].find(searchKey) != -1 ):
			search_list.append({'domain' : ele['hostname'], 'api':'flippa.com', 'html_url' : ele['html_url']} )

	headers = { "accept": "application/json" , "Authorization": "sso-key UzQxLikm_46KxDFnbjN7cQjmw6wocia:46L26ydpkwMaKZV6uVdDWe"}
	try:
		response = requests.get(godaddyUrl, headers=headers)
		godaddySearchResultData = response.json()
		# print(godaddySearchResultData)
		for ele in godaddySearchResultData['Products']:
			search_list.append({'domain' :  ''.join(searchKey.split())+'.'+ele['Tld'], 'api':'godaddy.com', 'html_url': 'https://uk.godaddy.com/dpp/find?checkAvail=0&tmskey=&domainToCheck='+searchKey})	
	except:
		print('godaddy err')
	return search_list


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
	uid = request.user.id
	userobj = User.objects.get(id=uid)
	# savedSearckKeys =  Searches.objects.all().select_related('campaign_id') 

	try:
		savedCampaigns = Campaigns.objects.filter(belongs_to = userobj)
		savedSearckKeys =  Searches.objects.filter(campaign_id__in = Campaigns.objects.filter(belongs_to = userobj))
	except: 
		savedCampaigns = []
	
		# savedSearckKeys = savedCampaigns.Searches.all()
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

		savedSearckKeys =  Searches.objects.filter(search_key = searchKey)
		print(savedSearckKeys)
		searchResultlist = makeSearchAPICall(searchKey)

		for i in searchResultlist:
			# print(i['domain'])
			result = SearchResults(result = i['domain'], search_key = savedSearckKeys[0])
			result.save()

		return HttpResponseRedirect("/profile")
	else:
		return HttpResponseRedirect("/")	
	


def newUser(request):
	try:
		errVal = request.GET.get('err')
		if errVal :
			return render(request, 'home/signup.html',{
				'title': 'Demo App',
				'showLogin' : 'false',
				'showLogout' : 'false',
				'showSignup' : 'false',
				'saveSearch' : 'falase',
				'searchKey'  : '',
				'message'	 : 'USERNAME ALREADY EXIST'
				})
		else:
			return render(request, 'home/signup.html',{
				'title': 'Demo App',
				'showLogin' : 'false',
				'showLogout' : 'false',
				'showSignup' : 'false',
				'saveSearch' : 'falase',
				'searchKey'  : '',
				'message'	 : ''
				})
	except :
		return render(request, 'home/signup.html',{
			'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'false',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			'message'	 : ''
			})

def saveNewUser(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	email = request.POST.get('email')

	try:
		user = User.objects.create_user(username=username, email=email, password=password)
		return HttpResponseRedirect("/")
	except:
		return HttpResponseRedirect("/newUser?err=1")
		