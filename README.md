# Продуктовый помощник (дипломный проект)


### Проект "**Продуктовый помощник**" это онлайн-сервис на котором пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.




### Запуск проекта в контейнерах:

В папке infra выполните команду для создания .env файла:

```py
echo '''DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
''' > .env
```

#### Сборка контейнеров
```
cd foodgram-project-react/infra/
docker-compose up -d --build
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
docker-compose exec backend python manage.py createsuperuser
docker-compose exec backend python manage.py load_tags
docker-compose exec backend python manage.py load_ingredients
```
