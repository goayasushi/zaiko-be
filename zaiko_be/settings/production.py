"""
本番環境用の設定
"""

from .base import *  # 共通設定をインポート
import requests
import os


# デバッグモードを無効に
DEBUG = False

# ALBヘルスチェック時にEC2のプライベートIPから送信されるため、動的に取得しALLOWED_HOSTSに追加
try:
    EC2_PRIVATE_IP = requests.get(
        "http://169.254.169.254/latest/meta-data/local-ipv4", timeout=1
    ).text
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)
except requests.exceptions.RequestException:
    # EC2メタデータにアクセスできない場合は無視
    pass

# ALB/プロキシ経由のリクエストを処理するための設定
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

# 本番環境ではSessionAuthentication認証は不要
# 基本設定を継承したまま使用（JWT認証のみ）

# 本番環境固有の追加設定
SESSION_COOKIE_SECURE = True  # セキュアCookieを使用
CSRF_COOKIE_SECURE = True  # CSRFトークンにセキュアCookieを使用

# 本番環境のセキュリティ設定
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# AWS S3 settings for media files
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME", "ap-northeast-1")
AWS_CLOUDFRONT_DOMAIN = os.getenv("AWS_CLOUDFRONT_DOMAIN")
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_S3_CUSTOM_DOMAIN = AWS_CLOUDFRONT_DOMAIN
MEDIA_URL = f"https://{AWS_CLOUDFRONT_DOMAIN}/"
