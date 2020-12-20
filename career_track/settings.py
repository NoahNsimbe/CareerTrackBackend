import os
import sys
import django_heroku

from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = os.environ.get("DEBUG", True)

# if not DEBUG:
#     env_path = os.path.join(os.path.dirname(__file__), '.env')
#     load_dotenv(env_path)

# if DEBUG:
#     ALLOWED_HOSTS = ['*']
#     SECRET_KEY = "9-s1-+vyfm5b9y=cupm#pq)c8z8+*squ4qd0bsyl!61jis&e^x"
# else:

ALLOWED_HOSTS = ['ancient-waters-88205.herokuapp.com', '127.0.0.1']
SECRET_KEY = os.environ.get("SECRET_KEY", "9-s1-+vyfm5b9y=cupm#pq)c8z8+*squ4qd0bsyl!61jis&e^x")

ADMINS = [("Noah Nsimbe", "nsimbenoah@gmail.com")]
CORS_ORIGIN_ALLOW_ALL = True

# if DEBUG:
#     CORS_ORIGIN_ALLOW_ALL = True
# else:
#     CORS_ORIGIN_WHITELIST = [
#         'http://localhost:3000', 'http://127.0.0.1:3000', 'http://0.0.0.0:3000', 'http://localhost', 'http://127.0.0.1',
#         'http://0.0.0.0',
#     ]

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'app.apps.MainAppConfig'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware'
]

FIXTURE_DIRS = (os.path.join(BASE_DIR, 'fixtures'),)

REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


ROOT_URLCONF = 'career_track.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'career_track.wsgi.application'

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True


# if DEBUG:
DATABASES = {
    'default': {
        'ENGINE': os.environ.get("DATABASE_ENGINE", "django.db.backends.postgresql"),
        'NAME': os.environ.get("DATABASE_NAME", "career_track"),
        'HOST': os.environ.get("DATABASE_HOST", "127.0.0.1"),
        'PORT': os.environ.get("DATABASE_HOST_PORT", 5432),
        'USER': os.environ.get("DATABASE_USER", "career_track"),
        'PASSWORD': os.environ.get("DATABASE_PASSWORD", "9@55w0r6"),
    }
}
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': os.getenv('DATABASE_ENGINE'),
#             'NAME': os.getenv('DATABASE_NAME'),
#             'USER': os.getenv('DATABASE_USER'),
#             'PASSWORD': os.getenv('DATABASE_PASSWORD'),
#             'HOST': os.getenv('DATABASE_HOST'),
#             'PORT': os.getenv('DATABASE_HOST_PORT'),
#         }
#     }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db'
#     }
# }

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_db'
    }


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

django_heroku.settings(locals())
