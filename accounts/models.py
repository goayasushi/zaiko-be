from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """ユーザーマネージャーのカスタムクラス。メールアドレスをユーザー名として使用"""

    def create_user(self, email, password=None, **extra_fields):
        """通常ユーザーを作成"""
        if not email:
            raise ValueError(_("メールアドレスは必須です"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """スーパーユーザーを作成"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("スーパーユーザーはis_staff=Trueである必要があります"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(
                _("スーパーユーザーはis_superuser=Trueである必要があります")
            )

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """カスタムユーザーモデル"""

    username = None  # usernameフィールドを無効化
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"  # 認証に使用するフィールド
    REQUIRED_FIELDS = []  # createsuperuserコマンド実行時に要求されるフィールド

    objects = CustomUserManager()

    def __str__(self):
        return self.email
