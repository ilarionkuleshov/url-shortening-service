from django.urls import path, include
from . import views


urlpatterns = [
	path('', views.main),
	path('shorten-url/', views.shorten_url, name='shorten_url'),
	path('redirect/<str:short_url>/', views.redirect),
	path('api/', include('shortener.api.urls'))
]
