from django.shortcuts import render
from django.http import HttpResponseRedirect

from .models import URL, Transition, create_url_object


def main(request):
	return render(request, 'shortener/main.html')


def shorten_url(request):
	url = create_url_object(request, request.POST['initial_url'])

	if url:
		return render(request, 'shortener/result.html', {'initial_url': url.initial_url, 'short_url': url.get_full_short_url(request)})
	else:
		return render(request, 'shortener/error.html', {'is_form': True, 'error_msg': 'Введите корректную ссылку...'})


def redirect(request, short_url):
	try:
		url = URL.objects.get(short_url=short_url)
	except:
		return render(request, 'shortener/error.html', {'is_form': False, 'error_msg': 'Такой ссылки не существует...'})

	if url.is_available():
		transition = Transition(url=url)
		transition.save(request)

		return HttpResponseRedirect(url.initial_url)

	else:
		return render(request, 'shortener/error.html', {'is_form': False, 'error_msg': 'Вы пытаетесь перейти по недоступной ссылке...'})
