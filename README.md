![Foodgram workflow](https://github.com/ansuleymanova/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

# Foodgram

App for posting, editing & favoriting recipes with a "shopping cart" function that provides a shopping list for all selected recipes. 

Powered by Django & React.

Temporarily hosted here: http://130.193.55.155

## How To

The repo contains files necessary to build three Docker containers on your machine: postgres, nginx and the backend app. The container for frontend will start and then terminate after front is built.

Clone the repo and from ```infra``` folder run following commands:

### Startup

```
docker-compose up --build -d
docker-compose exec web python manage.py makemigrations users
docker-compose exec web python manage.py makemigrations titles
docker-compose exec web python manage.py makemigrations reviews
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --no-input
```

### Superuser

```
docker-compose exec web python manage.py createsuperuser
```

### Fixtures

From ```backend``` folder:

```
docker-compose exec web python manage.py loaddata ingredients.json
```

The server is up, go ahead and try http://127.0.0.1/admin
