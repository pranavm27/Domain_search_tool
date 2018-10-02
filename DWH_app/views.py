from django.shortcuts import render
from django.http import HttpResponse
from .models import Searches, Campaigns
import requests

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
	searchKey =request.GET.get('key' )
	print(searchKey)
	print(searchKey.strip())
	flippaApiUrl = 'https://api.flippa.com/v3/listings?query=' + searchKey.replace(" ", "")
	print(flippaApiUrl)
	response = requests.get(flippaApiUrl)
	searchResultData = response.json()
	if request.user.is_authenticated:
		return render(request, 'home/search.html',{
			'title': 'Demo App',
				'showLogin' : 'false',
				'showLogout' : 'true',
				'showSignup' : 'false',
				'saveSearch' : 'true',
				'searchKey'  : searchKey,
				'flippaSearchResultData' : searchResultData['data']
				})

	return render(request, 'home/search.html',{
		'title': 'Demo App',
			'showLogin' : 'true',
			'showLogout' : 'falaSe',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : searchKey,
			'flippaSearchResultData' : searchResultData['data']
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
	savedCampaigns = Campaigns.objects.all()
	
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
	newCampaign = Campaigns(name = campaignName , campaign_type= campaignType, start = campaignStart, end = campaignEnd )
	newCampaign.save()

	savedSearckKeys =  Searches.objects.all()
	savedCampaigns = Campaigns.objects.all()
	return render(request, 'home/profile.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'false',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			'searchResultData' : savedSearckKeys,
			'savedCampaigns'	: savedCampaigns
			})



def campaignOverview(request):
	savedCampaigns = Campaigns.objects.all()
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
	searchKey =  Campaigns.objects.get(id = searchKeyId)
	searchKey.delete()
	savedCampaigns = Campaigns.objects.all()
	return render(request, 'home/campaignOverview.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'false',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			'savedCampaigns'	: savedCampaigns
			})


