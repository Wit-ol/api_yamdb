import os
from csv import DictReader

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ('Добавляет в бд данные из csv файла',
            'Аргумент 1 - название csv файла без расширения',
            'Аргумент 2 - название модели')

    def add_arguments(self, parser):
        parser.add_argument('csv_file', nargs='+', type=str)
        parser.add_argument('model_name', nargs='+', type=str)

    def handle(self, *args, **options):
        model = apps.get_model(app_label='reviews',
                               model_name=options['model_name'][0])
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        rel_path = f'static\\data\\{options["csv_file"][0]}.csv'
        abs_file_path = os.path.join(fileDir, rel_path)
        with open(abs_file_path, encoding='utf-8') as csvfile:
            reader = DictReader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                # model.objects.create(**row) # Применяется если нет ForeignKey
                model.objects.create(id=row['id'],
                                     text=row['text'],
                                     pub_date=row['pub_date'],
                                     author_id=row['author'],
                                     title_id=row['title_id'],
                                     score=row['score']
                                     )
