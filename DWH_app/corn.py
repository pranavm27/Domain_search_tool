import smtplib
from .models import Searches, Campaigns, SearchResults
import requests
from django.contrib.auth.models import User

def my_scheduled_job():
	searchKey = Searches.objects.all();
	for key in searchKey:
		newResults = makeSearchAPICall(key)
		checkIfDomainIsPresent(newResults,key)
	return

def sendemail(toEmail, name, newResult):
	sender = 'pranav.query@gmail.com'
	to = toEmail

	message = "	Hello " + name + " there is a "+newResult+" available for purchase , please click the below link to buy it."

	try:
		smtpObj = smtplib.SMTP('smtp.gmail.com')
		smtpObj.sendmail(sender, to, message)
		print "Successfully sent email"
	except SMTPException:
		print "Error: unable to send email"
	return

def makeSearchAPICall(key):
	search_list = []
	searchKey = key
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
	return search_list


def checkIfDomainIsPresent(newResults, key):
	oldResults = SearchResults.objects.all()
	for oldResult in oldResults:
		for newResult in new newResult:
			if oldResult !== newResult:
				sendemail(key.email, key.username, newResult)
	return