"""
CI環境用の設定
"""

from .base import *  # 共通設定をインポート
import tempfile

# デバッグモードを無効に
DEBUG = False


# テスト環境用のメディアファイル設定
# テスト中に一時ディレクトリを使用
MEDIA_ROOT = tempfile.mkdtemp()
MEDIA_URL = "/media/"

# テスト用のファイルストレージ
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
