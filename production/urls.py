from django.conf.urls import url
from production import views

urlpatterns = [
    url(r'^all', views.ProductionList.as_view()),
    url(r'^create', views.ProductionCreate.as_view()),
    url(r'^(?P<pk>[0-9]+)/', views.ProductionDetail.as_view()),
]
