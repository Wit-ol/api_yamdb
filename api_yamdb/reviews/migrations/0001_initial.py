# Generated by Django 2.2.16 on 2022-03-10 16:08

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Музыка', 'Музыка'), ('Книги', 'Книги'), ('Фильм', 'Фильм')], max_length=10)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Ваш коммент тут. Обязательное поле.', verbose_name='Текст комментария')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации комментария')),
            ],
            options={
                'verbose_name': 'Комментарий к отзыву',
                'verbose_name_plural': 'Комментарии к отзывам',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Драма', 'Драма'), ('Комедия', 'Комедия'), ('Вестерн', 'Вестерн'), ('Фэнтези', 'Фэнтези'), ('Фантастика', 'Фантастика'), ('Детектив', 'Детектив'), ('Триллер', 'Триллер'), ('Сказка', 'Сказка'), ('Гонзо', 'Гонзо'), ('Роман', 'Роман'), ('Баллада', 'Баллада'), ('Сказка', 'Сказка'), ('Rock-n-roll', 'Rock-n-roll'), ('Классика', 'Классика'), ('Рок', 'Рок'), ('Шансон', 'Шансон'), ('Ужасы', 'Ужасы')], max_length=10)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Ваш отзыв тут. Обязательное поле.', verbose_name='Текст отзыва')),
                ('pub_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации отзыва')),
                ('score', models.PositiveSmallIntegerField(help_text='Ваша оценка произведению (1-10) Обязательное поле.', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('year', models.PositiveIntegerField(db_index=True, validators=[django.core.validators.MaxValueValidator(2022)])),
                ('description', models.TextField(blank=True, max_length=200, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_of_title', to='reviews.Category', verbose_name='Категория')),
                ('genre', models.ManyToManyField(through='reviews.GenreTitle', to='reviews.Genre')),
            ],
        ),
    ]
