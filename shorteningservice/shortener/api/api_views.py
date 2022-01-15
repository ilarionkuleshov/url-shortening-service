from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import URL, create_url_object


class URLApiView(APIView):

	def post(self, request):
		url = create_url_object(request, request.data['initial_url'])

		return Response({'short_url': url.short_url})

	def get(self, request):
		url = URL.objects.get(short_url=request.data['short_url'])
		details = url.get_statistics(request)

		return Response(details)

	def delete(self, request):
		url = URL.objects.get(short_url=request.data['short_url'])
		details = url.delete(request)

		return Response(details)
