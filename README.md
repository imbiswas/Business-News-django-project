# Business News Site:

## Environment Setup:

- Install `requirements.txt`
- Install postgresql

## Running in local Machine

- Create a Database in postgresql by the name : **hamrobiz**

### Migrations Process:

```console
python manage.py makemigrations
python manage.py migrate
python manage.py migrate --run-syncdb
```

### Execute the following queries in hamrobiz :

```sql
SELECT * FROM hitcount_hit_count;

ALTER TABLE hitcount_hit_count
ALTER COLUMN object_pk TYPE INT USING object_pk::integer;
```

## Adding news from news24:

- Create a folder name `downloaded_images` inside `media` (which is present in the same directory as `manage.py`)

```console

> python manage.py shell

>>> tags = ['technology', 'festival', 'electronics', 'economics','general', 'business', 'gadgets']
>>> from news.models import Images, Category
>>> from django.utils.text import slugify
>>>
>>> for t in tags:
...     Category.objects.create(title = t, slug = slugify(t))
...
<Category: technology>
<Category: festival>
<Category: electronics>
<Category: economics>
<Category: general>
<Category: business>
<Category: gadgets>
>>> from home import news24scraper
>>> news24scraper.loadOnce()
```
