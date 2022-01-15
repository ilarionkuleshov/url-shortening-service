import random
from string import ascii_letters, digits

import requests


CHAR_LIST = ascii_letters + digits + '-'


def generate_short_url(URL, max_length=6):
	current_length = random.choice(range(1, max_length+1))
	short_url = ''

	for _ in range(current_length):
		short_url += random.choice(CHAR_LIST)

	try:
		URL.objects.get(short_url=short_url)
		return generate_short_url(URL, max_length)

	except:
		return short_url


def get_full_url(url):
	if not url.split(':')[0] in ['http', 'https']:
		url = f'http://{url}'

	try:
		return requests.get(url).url
	except:
		return None


def get_client_identifier(request):
	if request.user.is_authenticated:
		id = request.user.id
		identifier = f'ID {id}'

	else:
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')

		identifier = f'IP {ip}'

	return identifier
