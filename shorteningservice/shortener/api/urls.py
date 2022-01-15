from django.urls import path

from .api_views import URLApiView


urlpatterns = [
	path('', URLApiView.as_view())
]
