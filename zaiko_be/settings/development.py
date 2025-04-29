"""
開発環境用の設定
"""

from .base import *  # 共通設定をインポート

# デバッグモードを有効に
DEBUG = True

# 開発環境専用のアプリを追加
INSTALLED_APPS += [
    "debug_toolbar",
]

# 開発環境専用のミドルウェアを追加
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Debug Toolbarを追加
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "zaiko_be.middleware.refresh_jwt.RefreshJWTMiddleware",
]

# 開発環境専用の認証設定 - SessionAuthenticationを追加
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",  # 開発環境のみ
    ),
    "DEFAULT_PAGINATION_CLASS": "zaiko_be.pagination.CustomPagination",
    "PAGE_SIZE": 20,
}

# Debug Toolbar設定
INTERNAL_IPS = type("i", (), {"__contains__": lambda *a: True})()

# 開発環境用のロギング設定（より詳細なログを出力）
LOGGING["loggers"].update(
    {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "INFO",  # 必要に応じて "DEBUG" に変更するとSQLクエリが表示されます
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    }
)

# Media files settings (in base settings)
MEDIA_ROOT = "/app/media"
MEDIA_URL = "/media/"

# Default file storage
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
