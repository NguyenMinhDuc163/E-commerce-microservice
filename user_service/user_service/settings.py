from pathlib import Path
import os
from dotenv import load_dotenv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'YOUR_DJANGO_SECRET_KEY_HERE_USER_SERVICE'
REFRESH_TOKEN_SECRET = 'YOUR_JWT_REFRESH_SECRET_HERE'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

PORT = 8002
CORS_ALLOW_ALL_ORIGINS = True
ALLOWED_HOSTS = ['*']
CORS_ALLOW_CREDENTIALS = True

# Disable ALLOWED_HOSTS validation completely for Docker
USE_L10N = True
ALLOWED_HOSTS = ['*']  # Allow all hosts

# Additional debug settings
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'user_model',
    'user_info',
    'user_login',
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'user_service.urls'
SPECTACULAR_SETTINGS = {
    'TITLE': 'User Service API',
    'DESCRIPTION': 'API documentation for User Service',
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
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': [],  # Tạm thời tắt
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Tạm thời cho phép tất cả
    ],
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': [
    #     'rest_framework_simplejwt.authentication.JWTAuthentication',
    # ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',  # Thêm dòng này
    # ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}
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

WSGI_APPLICATION = 'user_service.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'user_service',  # Tên database bạn đã tạo
#         'USER': 'root',      # Tên user MySQL
#         'PASSWORD': 'NguyenDuc@163',  # Mật khẩu MySQL
#         'HOST': 'localhost',   # Địa chỉ host MySQL (thường là localhost)
#         'PORT': '3306',        # Cổng MySQL (mặc định là 3306)
#     }
# }
if not os.environ.get('DJANGO_DOCKER_ENV'):
   load_dotenv()

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': os.environ.get('DATABASE_NAME', 'user_service'),
       'USER': os.environ.get('DATABASE_USER', 'root'),
       'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'YOUR_MYSQL_PASSWORD_HERE'),
       'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
       'PORT': os.environ.get('DATABASE_PORT', '3306'),
       'OPTIONS': {
           'charset': 'utf8mb4',
           # Thêm các tùy chọn kết nối MySQL
           'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
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

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
