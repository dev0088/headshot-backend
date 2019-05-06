"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic.base import TemplateView
from django.conf import settings
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_swagger.views import get_swagger_view
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import renderers, response, schemas
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

swagger_schema_view = get_swagger_view(title='Headshot printing API')

schema_view = get_schema_view(
   openapi.Info(
      title="Headshot API",
      default_version='v1',
      description="RESTful API for www.headshotprinting.net",
      terms_of_service="http://www.headshotprinting.net/terms/",
      contact=openapi.Contact(email="alaric@headshot.com"),
      license=openapi.License(name="headshotprinting.net"),
   ),
   # validators=['flex', 'ssv'],
   url="http://www.headshotprinting.net/api/v1",
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
	# url(r'^apis', schema_view),
    url(r'^apis(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^apis/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^swagger-docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'^admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),
	url(r'^api/v1/auth/', include('authentication.urls')),
    url(r'^api/v1/productions/', include('production.urls')),
    url(r'^api/v1/quantity/', include('quantity.urls')),
    url(r'^api/v1/headshot/', include('headshot.urls')),
    url(r'^api/v1/stripe_payments/', include('stripe_payment.urls')),
]
