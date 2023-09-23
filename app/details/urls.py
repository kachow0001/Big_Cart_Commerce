from django.urls import path 
from . import views 

#URLConf Module
#Import URLConf into main url of project

urlpatterns = [
    path('info/',views.first_display)
]
