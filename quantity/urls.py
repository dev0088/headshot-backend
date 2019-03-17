from django.conf.urls import url
from quantity import views

urlpatterns = [
    url(r'^all', views.QuantityList.as_view()),
    url(r'^create', views.QuantityCreate.as_view()),
    url(r'^(?P<pk>[0-9]+)/', views.QuantityDetail.as_view()),
]
