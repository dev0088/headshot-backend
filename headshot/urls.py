from django.conf.urls import url
from headshot import views

urlpatterns = [
    url(r'^all', views.HeadshotList.as_view()),
    url(r'^create', views.HeadshotCreate.as_view()),
    url(r'^upload_image/(?P<pk>[0-9]+)/', views.HeadshotUploadImage.as_view()),
    url(r'^upload_doc/(?P<pk>[0-9]+)/', views.HeadshotUploadDoc.as_view()),
    url(r'^charge/(?P<pk>[0-9]+)/', views.HeadshotPayment.as_view()),
    url(r'^(?P<pk>[0-9]+)/', views.HeadshotDetail.as_view()),
]
