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
CLOUDFLARE_TURNSTILE_SITE_KEY='0x4AAAAAAAzjzxzoQg_8PLIQ'
CLOUDFLARE_TURNSTILE_SECRET_KEY='0x4AAAAAAAzjz_yg4Ic4WuiMaNbaIviOpac'
SESSION_COOKIE_AGE = 600
SESSION_SAVE_EVERY_REQUEST = True