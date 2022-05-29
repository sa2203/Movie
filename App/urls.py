# import libraries
from . import views
from django.urls import path

# url patterns for the views created
urlpatterns = [
     path('', views.home, name="home"),
     path('recommend/<str:param>', views.recommendations, name="recommed")
]