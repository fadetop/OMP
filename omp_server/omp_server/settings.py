"""
Django settings for omp_server project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
import random
import datetime
from pathlib import Path
from utils.parse_config import OMP_MYSQL_HOST, OMP_MYSQL_PORT, \
    OMP_MYSQL_USERNAME, OMP_MYSQL_PASSWORD, TOKEN_EXPIRATION, \
    SSH_CMD_TIMEOUT, PRIVATE_KEY

SSH_CMD_TIMEOUT = SSH_CMD_TIMEOUT
PRIVATE_KEY = PRIVATE_KEY
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.dirname(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'rofvdj3gbyg0(vb-ck=d(*1o=jx=l2_%c0*ox^rv%2s36(u3-@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 允许所有
ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',
    'db_models',
    'users',
    'tests',
    'inspection',
    'service_upgrade',
    'tool',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'utils.middleware_handler.RoleAuthenticationMiddleware',
    'utils.middleware_handler.OperationLogMiddleware'
]

ROOT_URLCONF = 'omp_server.urls'

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

WSGI_APPLICATION = 'omp_server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'omp',
        'USER': OMP_MYSQL_USERNAME,
        'PASSWORD': OMP_MYSQL_PASSWORD,
        'HOST': OMP_MYSQL_HOST,
        'PORT': int(OMP_MYSQL_PORT),
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
            "NAME": f"test_omp_{random.randint(100, 200)}"
        },
        'OPTIONS': {
            'init_command': 'SET sql_mode=STRICT_TRANS_TABLES',
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# DRF 相关设置
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
    ),
    "EXCEPTION_HANDLER": "utils.exception_handler.common_exception_handler",
    "DEFAULT_RENDERER_CLASSES": (
        "utils.response_handler.APIRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
}

# JWT相关设置
JWT_AUTH = {
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=int(TOKEN_EXPIRATION)),
    "JWT_ALLOW_REFRESH": True,
    "JWT_AUTH_COOKIE": "jwtToken",
}

AUTH_USER_MODEL = "db_models.UserProfile"

# celery 相关配置
CELERY_RESULT_BACKEND = "django-db"
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = TIME_ZONE
DJANGO_CELERY_BEAT_TZ_AWARE = False
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_IMPORTS = ("hosts.tasks", "inspection.tasks")

LOGGER_CLASS = 'concurrent_log_handler.ConcurrentRotatingFileHandler'
LOG_BACKUP_SIZE = 1024 * 1024 * 100
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s][%(levelname)s] %(pathname)s %(lineno)d -> %(message)s'}
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level': 'DEBUG',
            'class': LOGGER_CLASS,
            'filename': os.path.join(PROJECT_DIR, "logs/debug.log"),  # 日志输出文件
            'maxBytes': LOG_BACKUP_SIZE,  # 文件大小
            'backupCount': 5,  # 备份份数
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
        'error': {
            'level': 'ERROR',
            'class': LOGGER_CLASS,
            'filename': os.path.join(PROJECT_DIR, "logs/error.log"),
            'maxBytes': LOG_BACKUP_SIZE,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'DEBUG',
            'class': LOGGER_CLASS,
            'filename': os.path.join(PROJECT_DIR, "logs/request.log"),
            'maxBytes': LOG_BACKUP_SIZE,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['request_handler'],
            'level': 'INFO',
            'propagate': True,
        },
        'server': {
            'handlers': ['default', 'error'],
            'level': "INFO",
            'propagate': True
        }
    }
}
# DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# grafana跳转使用
X_FRAME_OPTIONS = 'SAMEORIGIN'

# 发邮件使用,是否使用ssl，使用端口：465/994 不使用：25
EMAIL_USE_SSL = True

# 可定制化指标的服务及指标
CUSTOM_THRESHOLD_SERVICES = {
    "kafka": {"kafka_consumergroup_lag"}
}

# 备份相关配置
# 可备份的组件
BACKUP_SERVICE = {"mysql", "arangodb", "postgreSql"}
BACKUP_DEFAULT_PATH = os.path.join(PROJECT_DIR, "data/backup/")

SCAN_TOOL_LOCK_KEY = "tool_package_verify"

INTERFACE_KINDS = {"/api/appStore/upload/": "修改",
                   "/api/appStore/remove/": "删除",
                   "/api/appStore/publish/": "修改",
                   "/api/appStore/executeLocalPackageScan/": "修改",
                   "/api/appStore/deploymentPlanValidate/": "查看",
                   "/api/appStore/deploymentPlanImport/": "增加",
                   "/api/appStore/createInstallInfo/": "增加",
                   "/api/appStore/executeInstall/": "增加",
                   "/api/appStore/checkInstallInfo/": "查看",
                   "/api/appStore/createServiceDistribution/": "增加",
                   "/api/appStore/checkServiceDistribution/": "查看",
                   "/api/appStore/createInstallPlan/": "新增",
                   "/api/appStore/createComponentInstallInfo/": "新增",
                   "/api/appStore/retryInstall/": "修改",
                   "/api/backups/backupSettings/": "修改",
                   "/api/backups/backupOnce/": "新增",
                   "/api/backups/backupHistory/": "删除",
                   "/api/backups/backupSendEmail/": "新增",
                   "/api/hosts/hosts/": "修改",
                   "/api/hosts/fields/": "查看",
                   "/api/hosts/maintain/": "修改",
                   "/api/hosts/restartHostAgent/": "修改",
                   "/api/hosts/batchValidate/": "查看",
                   "/api/hosts/batchImport/": "新增",
                   "/api/hosts/hostInit/": "修改",
                   "/api/hosts/hostsAgentStatus/": "查询",
                   "/api/hosts/hostReinstall/": "修改",
                   "/api/hosts/monitorReinstall/": "修改",
                   "/api/inspection/history/": "查询",
                   "/api/inspection/crontab/": "新增",
                   "/api/inspection/inspectionSendEmailSetting/": "修改",
                   "/api/inspection/inspectionSendEmail/": "查询",
                   "/api/promemonitor/monitorurl/": "修改",
                   "/api/promemonitor/updateAlert/": "修改",
                   "/api/promemonitor/restartMonitorAgent/": "修改",
                   "/api/promemonitor/globalMaintain/": "修改",
                   "/api/promemonitor/receiveAlert/": "新增",
                   "/api/promemonitor/updateSendEmailConfig/": "修改",
                   "/api/promemonitor/updateSendAlertSetting/": "新增",
                   "/api/promemonitor/hostThreshold/": "修改",
                   "/api/promemonitor/serviceThreshold/": "修改",
                   "/api/promemonitor/customThreshold/": "修改",
                   "/api/upgrade/do-upgrade/": "修改",
                   "/api/rollback/do-rollback/": "修改",
                   "/api/services/action/": "修改",
                   "/api/services/delete/": "查询",
                   "/api/services/SelfHealingSetting/": "修改",
                   "/api/services/UpdateSelfHealingHistory/": "修改",
                   "/api/users/users/": "新增",
                   "/api/users/updatePassword/": "修改"
                   }

# for automated testing
DATA_JSON_SECRET = "Yunweiguanli@OMP_123"
