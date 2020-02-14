# Django on Heroku with AWS S3 bucket for uploading files


## Creating a Django project & App
[django-tutorial](https://docs.djangoproject.com/en/3.0/intro/tutorial01/)

Follow this:
```
$ django-admin startproject mysite
$ python manage.py startapp polls
```
The directory structure will like this


![](https://i.imgur.com/jtu4MkJ.jpg =50%x)

---


## Setting the home page
- Add templates folder to mysite
- Write **index.html**
```html=
<html>
    <head>File Uploads</head>
    <body>
        <form enctype="multipart/form-data" action="" method="post">
            {% csrf_token %}
            {{ form }}
            <input type="file" name="file"/>
            <input type="submit" value="Save">
        </form>
    </body>
</html>
```
The directory structure will like this

![](https://i.imgur.com/AzaK1kQ.jpg)

### settings .py
```python=33
INSTALLED_APPS = [
      ..
      ..
      ..
    'polls',
]
```
```python=54
TEMPLATES = [
    {
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ............................
        ............................
    }
]
```

### views .py
```python=
from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'index.html')
```

### urls .py
```python=16
from django.contrib import admin
from django.urls import path
from polls.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
]
```

### Testing
```
$ python manage.py runserver
```

You can see the link : http://127.0.0.1:8000/index/

![](https://i.imgur.com/3SQULxe.jpg)

---

## Heroku

### setting .py
```python=28
ALLOWED_HOSTS = ['*']
```

### Procfile
```
web: gunicorn mysite.wsgi
```
### requirements.txt
```

```
### runtime.txt
```
python-3.6.10
```

Try to push
```
$ git init
$ heroku login
$ heroku git:remote -a yourname
$ heroku config:set DISABLE_COLLECTSTATIC=1
$ git add .
$ git commit -am "make it better"
$ git push heroku master
```

You can see the link : https://***.herokuapp.com/index/

---

## Database
The example use the [Heroku Postgres](https://elements.heroku.com/addons/heroku-postgresql)

![](https://i.imgur.com/xpAK6Cr.jpg =40%x)
```
$ heroku config:set DATABASE_HOST=xxx
$ heroku config:set DATABASE_NAME=xxx
$ heroku config:set DATABASE_USER=xxx
$ heroku config:set DATABASE_PORT=xxx
$ heroku config:set DATABASE_PASSWORD=xxx
```


### setting .py
```python=76
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}
```
### models .py
> upload_to='profile_pics'
>> upload the file to AWS s3 profile_pics folder
```python=
from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='profile_pics')
```

---

## AWS S3 setup
[Using AWS S3 to Store Static Assets and File Uploads](https://devcenter.heroku.com/articles/s3)
```
$ heroku config:set AWS_ACCESS_KEY_ID=xxx AWS_SECRET_ACCESS_KEY=yyy
$ heroku config:set S3_BUCKET_NAME=appname-assets
```

### settings .py
```python=33
INSTALLED_APPS = [
      ..
      ..
      ..
    'storages',
]
```

Add the block code to setting
```python=126
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
```

### views .py
Add the function to views
```python=
from django.shortcuts import render
from .models import Image

# Create your views here.
def index(request):
    if request.method == 'POST':
        image_file = request.FILES.get('file', False)
        if image_file:
            upload = Image(image=image_file)
            upload.save()
        else:
            print('error')
    return render(request, 'index.html')
```
Try to push
```
$ git add .
$ git commit -am "make it better"
$ git push heroku master
$ heroku run python manage.py makemigrations 
$ heroku run python manage.py migrate
```

*The error : django.db.utils.ProgrammingError: relation "yourTable" does not exist*

**Try this**
```
$ heroku run python manage.py migrate --run-syncdb
```

Now, you can try to upload file