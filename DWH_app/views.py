from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Searches, Campaigns, SearchResults
import requests
import xml.etree.ElementTree as ET
import difflib
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
		'showLogin' : 'false',
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
			'showLogin' : 'false',
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
	flippaApiUrl = 'https://flippa.com/v3/listings?search_template=most_relevant&query[keyword]='+searchKey+'&filter[property_type]=website,app,fba,business&page[size]=50&include=upgrades,tags_monetization,categories_top_level'
	godaddyAuctionUrl = 'https://uk.auctions.godaddy.com/trpSearchResults.aspx'
	sedoUrl = 'https://api.sedo.com/api/sedointerface.php?action=DomainSearch&partnerid=323505&signkey=26d24c95ed713ef6b46ed3d747e312&keyword=' + searchKey
	enomUrl = 'https://www.enom.com/beta/api/domains/'+searchKey+'/recommended?count=50&onlyga=false'
	afternicUrl = 'https://www.afternic.com/search?k='+searchKey+'&tld=com'
	
	#try flippa
	try:
		response = requests.get(flippaApiUrl)
		flippaSearchResultData = response.json()
		for ele in flippaSearchResultData['data']:
			business_model =''
			industry = ''
			propertyType = ''
			try:
				business_model = ele['business_model']
			except :
				business_model = -1

			try:
				industry = ele['industry']
			except :
				industry = -1

			try:
				propertyType = ele['property_type']
			except :
				propertyType = -1

			tags = [ business_model , industry, propertyType]
			search_list.append({'domain' : ele['hostname'], 'tags': tags,  'api':'flippa.com', 'html_url' : ele['html_url']} )
	except :
		print('flippa err')

	#try enom
	try:
		response = requests.get(enomUrl)
		enomUrlSearchResultData = response.json()
		for ele in enomUrlSearchResultData['suggestions']['domains']:
			business_model = -1
			industry = ''
 			
			try:
				industry = ele['source']
			except :
				industry = -1

			tags = [ business_model , industry]
			search_list.append({'domain' : ele['domain'], 'tags': [],  'api':'enom.com', 'html_url' :'https://www.enom.com/domains/search-results?query='+searchKey})
	except :
		print('enom err')

	#try sedo
	try:
		headers = { "accept": " text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" }
		response = requests.get(sedoUrl)
		sedoSearchResultData = response
		tree = root = ET.fromstring(sedoSearchResultData.content)
		for child in root.findall('item'):
			business_model =''
			industry = -1

			try:
				business_model = 'Domain'
			except :
				business_model = -1


			tags = [ business_model , industry]
			search_list.append({'domain' : child.find('domain').text, 'tags': [],  'api':'sedo.com', 'html_url' : child.find('url').text} )
	except :
		print('sedo err')

	#try godaddy
	try:
		headers = { "accept": "application/x-www-form-urlencoded" }
		payload = {'t': '22', 'action': 'search', 'hidAdvSearch': 'ddlAdvKeyword:1|txtKeyword:'+ searchKey.replace(' ', ','), 'rtr': '4', 'baid': '-1', 'searchDir': '1', 'rnd': '0.4567284293006555', 'ZaYGLEV': 'ef2c269'}
		response = requests.post(godaddyAuctionUrl, headers = headers, data= payload)
		
		soup = BeautifulSoup(response.content)
		arr_list = soup.find_all("span", class_="OneLinkNoTx")

		for elm in arr_list:
			miid = elm.img.extract()
			miid = miid.get('id').split('_')[1]
			search_list.append({'domain' :  elm.text, 'tags': [],  'api':'godaddy.com', 'html_url': 'https://in.auctions.godaddy.com/trpItemListing.aspx?miid='+miid})

	except :
		raise print('godaddy err')
	
	#try afternic
	try:
		headers = { "accept": "application/x-www-form-urlencoded" }
		response = requests.get(afternicUrl, headers = headers)
		soup = BeautifulSoup(response.content)
		print( soup )
		arr_list = soup.find_all("div", class_="search-domain-wrap")
		print( arr_list )
		for elm in arr_list:
			search_list.append({'domain' :  elm.text, 'tags': [],  'api':'afternic.com', 'html_url': 'https://www.afternic.com/domain/'+elm.text})
	except :
		raise print('afternic err')
		
	sorted_search_list = sorted(search_list['domain'], key=lambda z: difflib.SequenceMatcher(None, z.lower(),searchKey).ratio(), reverse=True)
	return sorted_search_list


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
		nextVal = request.GET.get('next')
		if errVal :
			return render(request, 'home/signup.html',{
				'title': 'Demo App',
				'showLogin' : 'false',
				'showLogout' : 'false',
				'showSignup' : 'false',
				'saveSearch' : 'falase',
				'searchKey'  : '',
				'message'	 : 'USERNAME ALREADY EXIST',
				'next'		 : nextVal
				})
		else:
			return render(request, 'home/signup.html',{
				'title': 'Demo App',
				'showLogin' : 'false',
				'showLogout' : 'false',
				'showSignup' : 'false',
				'saveSearch' : 'falase',
				'searchKey'  : '',
				'message'	 : '',
				'next'		 : nextVal
				})
	except :
		return render(request, 'home/signup.html',{
			'title': 'Demo App',
			'showLogin' : 'false',
			'showLogout' : 'false',
			'showSignup' : 'false',
			'saveSearch' : 'falase',
			'searchKey'  : '',
			'message'	 : '',
			'next'		 : nextVal
			})

def saveNewUser(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	email = request.POST.get('email')
	next = request.POST.get('next')

	try:
		user = User.objects.create_user(username=username, email=email, password=password)
		return HttpResponseRedirect("accounts/login?next="+next)
	except:
		return HttpResponseRedirect("/newUser?err=1")
		