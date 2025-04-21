"""
環境に応じた設定ファイルを選択するためのエントリーポイント
"""

import os
import logging
import sys
import multiprocessing

# 標準出力へのロガーを設定（Docker環境でも確実に出力されるように）
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s %(module)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

# ロガーを取得
logger = logging.getLogger(__name__)

# DJANGO_SETTINGS_MODULE環境変数が設定されていれば、それを尊重
# 設定されていなければ、環境変数DJANGO_ENVの値に基づいて設定ファイルを選択
env = os.getenv("DJANGO_ENV", "development")

# 現在のプロセスIDとプロセス名を取得してログに含める
current_process = multiprocessing.current_process()
process_info = f"PID: {os.getpid()}, Process: {current_process.name}"

if env == "production":
    from .production import *

    logger.info(
        f"本番環境(production)の設定ファイルが読み込まれました [{process_info}]"
    )
else:
    from .development import *

    logger.info(
        f"開発環境(development)の設定ファイルが読み込まれました [{process_info}]"
    )
