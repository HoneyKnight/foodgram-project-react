from django.core.management import BaseCommand
from recipes.models import Tag


class Command(BaseCommand):
    help = 'Создание тегов в базе данных.'

    def handle(self, *args, **kwargs):
        data = [
            {'name': 'Завтрак', 'color': '#3DD25A', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#10B7FF', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#F61930', 'slug': 'dinner'},
        ]
        try:
            Tag.objects.bulk_create(Tag(**tag) for tag in data)
        except ValueError:
            print('Ошибка введенных данных.')
        else:
            print('Создание тегов окончено.')
