from django.shortcuts import render
from django.http import HttpResponse
from .models import Searches
import requests
# Create your views here.

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
	flippaApiUrl = 'https://api.flippa.com/v3/listings?query=' + searchKey 
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
				'searchResultData' : searchResultData['data']
				})

	return render(request, 'home/search.html',{
		'title': 'Demo App',
			'showLogin' : 'true',
			'showLogout' : 'falaSe',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : searchKey,
			'searchResultData' : searchResultData['data']
			})

def saveSearchKey(request):
	return render(request, 'home/profile.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'falaSe',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			'searchResultData' : ''
			})

def profile(request):
	return render(request, 'home/profile.html',{
		'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'falaSe',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			'searchResultData' : ''
			})