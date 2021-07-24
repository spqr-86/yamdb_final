# yamdb_final 
# Описание сервиса
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».<br>
![CI](https://github.com/spqr-86/yamdb_final/workflows/yamdb_workflow/badge.svg)<br>
![example workflow](https://github.com/spqr-86/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)


# Документация
http://178.154.208.254:81/redoc/

# Установка
1. Клонируйте репрозиторий ```https://github.com/spqr-86/yamdb_final```
2. Установите Docker (https://docs.docker.com/engine/install/)
3. Выполните ```docker-compose up -d --build```
4. Выполните:<br>
  ```docker-compose exec web python manage.py migrate --noinput```<br>
  ```docker-compose exec web python manage.py createsuperuser```<br>
  ```docker-compose exec web python manage.py collectstatic --no-input ```
5. Теперь проект доступен по адресу http://127.0.0.1/.

# Технологии
* Python
* Django
* Django REST
* Docker

#### Проект разработал:
* [Петр Балдаев](https://github.com/spqr-86)
