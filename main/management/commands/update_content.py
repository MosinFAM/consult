# your_app/management/commands/update_content.py

from django.core.management.base import BaseCommand
from main.models import Article
from main.utils.html_processor import enhance_html

class Command(BaseCommand):
    help = 'Обновляет HTML-контент всех статей в базе данных'

    def handle(self, *args, **kwargs):
        # Получаем все статьи
        articles = Article.objects.all()

        # Обновляем контент для каждой статьи
        for article in articles:
            article.content = enhance_html(article.content)
            article.save()

        self.stdout.write(self.style.SUCCESS('Все статьи успешно обновлены!'))
