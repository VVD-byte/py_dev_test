from django.contrib import admin
from django.urls import path
from .views import Purse, RegUser, Transact

urlpatterns = [
    path('purse/', Purse.as_view()),
    path('register/', RegUser.as_view()),
    path('trans/', Transact.as_view()),
]
