
from pathlib import Path
from datetime import timedelta
import os
import environ


env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

SECRET_KEY = env("SECRET_KEY")


ALLOWED_HOSTS = ["*"]

CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_ALLOW = True

CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:3000", 'http://localhost:3000']

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1:3000","http://localhost:3000","http://127.0.0.1:8000","http://localhost:8000" ]

# CORS_ORIGIN_WHITELIST = ['http://127.0.0.1:3000','http://localhost:3000']

CORS_ALLOW_ALL_ORIGINS = True

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

THIRD_PARTY_APPS=[
    "rest_framework",
    # "rest_framework.authtoken",
    "rest_framework_simplejwt",
    # "rest_framework_simplejwt.token_blacklist",
    # "dj_rest_auth",
    # "dj_rest_auth.registration",
    "corsheaders",
    "drf_yasg",

]
CUSTOM_APPS=[
    "users.apps.UsersConfig",
    "pets.apps.PetsConfig",
    "categories.apps.CategoriesConfig",
    "posts.apps.PostsConfig",
    "common.apps.CommonConfig",
    "images.apps.ImagesConfig",
    "auths.apps.AuthsConfig",
    "bookmarks.apps.BookmarksConfig",
    "likes.apps.LikesConfig",
]

SYSTEM_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

]
SITE_ID = 1

INSTALLED_APPS = SYSTEM_APPS + THIRD_PARTY_APPS + CUSTOM_APPS

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

REST_FRAMEWORK={
    # 'DEFAULT_PERMISSION_CLASSES': (#api 접근시에 인증된 유저(헤더에 access-tocken을 포함하여 유효한 유저만이 접근이 가능하게 함)
    #     'rest_framework.permissions.IsAuthenticated',
    # ),
    'DEFAULT_AUTHENTICATION_CLASSES':(
        # 'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 10,
}





# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


#Log
LOGGING={
    "version":1,
    "disable_existing_loggers":False,
    "formatters":{
        "verbose":{
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s" "%(process)d %(thread)d %(message)s"
        }
    },
    "handlers":{
        "console":{
            "level":"DEBUG",
            "class":"logging.StreamHandler",
            "formatter":"verbose"
        }
    },
    "root":{"level":"INFO", "handlers":{"console"}},
}
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_ROOT = "uploads"

MEDIA_URL = "user-uploads/"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "users.User"

GOOGLE_MAPS_API_KEY = env("GOOGLE_MAPS_API_KEY")
KAKAO_API_KEY=env("KAKAO_API_KEY")

CF_TOKEN=env("CF_TOKEN")
CF_ID=env("CF_ID")