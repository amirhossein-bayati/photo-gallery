# photo-gallery
This project is sample Django livewire photo gallery with Admin panel , Category , Comments, Photo share and more Capabilities 

![Default Home View](__screenshots/Home-page.png?raw=true "Title")

### Main features

* Separated dev and production settings

* Example app with custom user model

* Bootstrap static files included

* User registration and logging in

* Separated requirements files

* Share posts with email

* Contact Us form with sending an email to admin

* Get last 5 posts with postFeed

* Commenting for posts

* Search in posts with postgresql Search

* Use Category to see specific Posts

* Site map

# Getting Started
To use this template to start your own project:

clone the project

    git clone https://github.com/amirhossein-bayati/photo-gallery.git
    
create and start a a virtual environment

    virtualenv env --no-site-packages

    source env/bin/activate

Install the project dependencies:

    pip install -r requirements.txt

create a postgres db and add the credentials to settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'db_name',
            'USER': 'name',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    
then run

    python manage.py migrate

create admin account

    python manage.py createsuperuser
      
then

    python manage.py makemigrations

to makemigrations for the app

then again run

    python manage.py migrate

to start the development server

    python manage.py runserver

and open localhost:8000 on your browser to view the app.
