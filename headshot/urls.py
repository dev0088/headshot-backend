from django.conf.urls import url
from headshot import views

urlpatterns = [
    url(r'^all', views.HeadshotList.as_view()),
    url(r'^create', views.HeadshotCreate.as_view()),
    url(r'^upload/(?P<pk>[0-9]+)/', views.HeadshotUpload.as_view()),
    url(r'^(?P<pk>[0-9]+)/', views.HeadshotDetail.as_view()),
]
