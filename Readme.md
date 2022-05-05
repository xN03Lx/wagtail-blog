# Wagtail blog

## Requirements

    python >= 3.9

## Preparing the environment

Create your python environment (Linux)

```bash
python3 -m venv env
source env/bin/activate
```

## install dependencies

`pip install -r requirements.txt`

## Environment Prepare

Create your .env file
following the env-example file.

Configure your .env file

```bash
cp .env-example .env
```

## Run migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

## Run server

```bash
python manage.py runserver
```

## Urls

[http://localhost:8000/blog/](http://localhost:8000/blog/)  
[http://localhost:8000/login/](http://localhost:8000/login/)
