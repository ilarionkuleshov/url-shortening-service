from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from .logic import *


class URL(models.Model):

	initial_url = models.URLField('Исходная ссылка')
	short_url = models.CharField('Сокращенная ссылка', max_length=50)

	creator_identifier = models.CharField('Идентификатор создателя', max_length=50)

	transitions_n = models.PositiveIntegerField('Количество переходов', default=0)
	last_transition_time = models.DateTimeField('Время последнего перехода', null=True)

	is_deleted = models.BooleanField('is_deleted', default=False)

	def save(self, request=None, *args, **kwargs):
		if request:
			self.short_url = generate_short_url(URL)

		super().save(*args, **kwargs)

	def is_available(self):
		return not self.is_deleted

	def get_full_short_url(self, request):
		return f'http://{request.get_host()}/redirect/{self.short_url}/'

	def get_statistics(self, request):
		if not self.is_available():
			return {'details': 'Ошибка! Ссылка недоступна!'}
		elif get_client_identifier(request) == self.creator_identifier:
			return {'transitions_n': self.transitions_n}
		else:
			return {'details': 'Ошибка! Посмотреть статистку ссылки может только её создатель!'}

	def delete(self, request):
		if get_client_identifier(request) == self.creator_identifier:
			self.is_deleted = True
			self.save()

			return {'details': 'Ссылка успешно удалена!'}

		else:
			return {'details': 'Ошибка! Удалить ссылку может только её создатель!'}


class Transition(models.Model):

	url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='transitions')
	visitor_identifier = models.CharField('Идентификатор посетителя', max_length=50)

	def save(self, request, *args, **kwargs):
		self.visitor_identifier = get_client_identifier(request)

		try:
			self.url.transitions.get(visitor_identifier=self.visitor_identifier)
			return

		except:
			self.url.transitions_n += 1
			self.url.last_transition_time = timezone.now()
			self.url.save()

		super().save(*args, **kwargs)


def create_url_object(request, initial_url):
	initial_url = get_full_url(initial_url)
	creator_identifier = get_client_identifier(request)

	if initial_url:
		try:
			url = URL.objects.get(
				initial_url=initial_url,
				creator_identifier=creator_identifier
			)
			if not url.is_available():
				raise Exception('Error...')

		except:
			url = URL(initial_url=initial_url, creator_identifier=creator_identifier)
			url.save(request)

		return url

	else:
		return None
