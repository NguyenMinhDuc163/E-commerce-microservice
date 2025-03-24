from pathlib import Path
from dotenv import load_dotenv
import os

MONGODB_URI = os.environ.get('MONGODB_URI', 'mongodb+srv://nguyenduc:bMfuLqGps59NJLI8@cluster0.ld2i8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
MONGO_DB_NAME = os.environ.get('MONGODB_DB_NAME', 'book_app')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9hw0l$%)@9d%(-eqjm(+da(qw4)&@_qe78#)9irw%gf_oyu+l%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PORT = 8001
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ['*']

load_dotenv(os.path.join(BASE_DIR, '.env'))
MONGODB_URI = os.getenv("MONGODB_URI")
MONGO_DB_NAME = os.getenv("MONGODB_DB_NAME")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    "mobile.apps.MobileConfig",
    "book.apps.BookConfig",
    "clothes.apps.ClothesConfig",
    'drf_spectacular',
    'drf_spectacular_sidecar',  # Tùy chọn: Để sử dụng Swagger UI
]
SPECTACULAR_SETTINGS = {
    'TITLE': 'Product Service API',
    'DESCRIPTION': 'API documentation for Product Service',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
        'filter': True,
    },
}
REST_FRAMEWORK = {
    # Sử dụng Spectacular làm schema mặc định
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

    # Cấu hình phân trang (tùy chọn)
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'product_service.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'product_service.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'ENFORCE_SCHEMA': False,
#         'CLIENT': {
#             'host': MONGODB_URI,
#             'name': MONGO_DB_NAME,
#             'authMechanism': 'SCRAM-SHA-1',
#         }
#     },
#     'mongodb': {
#         'ENGINE': 'djongo',
#         'ENFORCE_SCHEMA': False,
#         'CLIENT': {
#             'host': MONGODB_URI,
#             'name': MONGO_DB_NAME,
#             'authMechanism': 'SCRAM-SHA-1',
#         }
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': MONGODB_URI,
            'name': MONGO_DB_NAME,
            'authMechanism': 'SCRAM-SHA-1',
        }
    },
    'mongodb': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': MONGODB_URI,
            'name': MONGO_DB_NAME,
            'authMechanism': 'SCRAM-SHA-1',
        }
    }
}
# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
