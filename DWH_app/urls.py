from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('saveSearchKey', views.saveSearchKey, name='saveSearchKey'),
    path('profile', views.profile, name=''),
    path('deleteKeyword', views.deleteKeyword, name=''),
    path('newCampaign', views.newCampaign, name=''),
    path('saveCampaign', views.saveCampaign, name=''),
    path('campaignOverview', views.campaignOverview, name=''),
    path('deleteCampaign', views.deleteCampaign, name=''),
    path('saveToCampaign', views.saveToCampaign, name=''),
    path('newUser', views.newUser, name=''),
    path('saveNewUser', views.saveNewUser, name=''),
]
