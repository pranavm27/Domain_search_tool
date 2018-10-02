from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('saveSearchKey', views.saveSearchKey, name='saveSearchKey'),
    path('profile', views.profile, name='profile'),
    path('deleteKeyword', views.deleteKeyword, name='profile'),
    path('newCampaign', views.newCampaign, name='profile'),
    path('saveCampaign', views.saveCampaign, name='profile'),
]
