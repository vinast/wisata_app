from wisata_project.settings_original import *

DEBUG = 1

DATABASES['default']['ENGINE']= 'django.db.backends.postgresql'
DATABASES['default']['NAME']= 'wisata_db'
DATABASES['default']['USER']= 'postgres'
DATABASES['default']['PASSWORD']= 'vinast111'
DATABASES['default']['HOST']= 'localhost'
DATABASES['default']['PORT']= 5432

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'wisata_app.Master_User'
CLOUDFLARE_TURNSTILE_SITE_KEY = '0x4AAAAAAAzWMysnlclxwmYa'
CLOUDFLARE_TURNSTILE_SECRET_KEY = '0x4AAAAAAAzWM4EjOX5aI5yhqVr5xIT7i0M'
SESSION_COOKIE_AGE = 12000
SESSION_SAVE_EVERY_REQUEST = True