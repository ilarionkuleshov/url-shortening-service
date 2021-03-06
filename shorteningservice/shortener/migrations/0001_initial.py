# Generated by Django 4.0.1 on 2022-01-15 01:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_url', models.URLField(verbose_name='Исходная ссылка')),
                ('short_url', models.CharField(max_length=50, verbose_name='Сокращенная ссылка')),
                ('creator_identifier', models.CharField(max_length=50, verbose_name='Идентификатор создателя')),
                ('transitions_n', models.PositiveIntegerField(default=0, verbose_name='Количество переходов')),
                ('last_transition_time', models.DateTimeField(null=True, verbose_name='Время последнего перехода')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is_deleted')),
            ],
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_identifier', models.CharField(max_length=50, verbose_name='Идентификатор посетителя')),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions', to='shortener.url')),
            ],
        ),
    ]
