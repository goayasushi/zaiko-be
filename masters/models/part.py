from django.db import models
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator


class Part(models.Model):
    """
    部品マスタモデル
    """

    # カテゴリの選択肢
    class Category(models.TextChoices):
        HEAD = "head", "ヘッド"
        SHAFT = "shaft", "シャフト"
        GRIP = "grip", "グリップ"
        OTHER = "other", "その他"

    # 基本情報
    name = models.CharField("部品名", max_length=200)
    category = models.CharField("カテゴリ", max_length=50, choices=Category.choices)

    # 仕入先情報（ForeignKey）
    supplier = models.ForeignKey(
        "masters.Supplier",
        on_delete=models.PROTECT,
        related_name="parts",
        verbose_name="仕入先",
    )

    # 価格情報
    cost_price = models.DecimalField(
        "原価",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    selling_price = models.DecimalField(
        "見積用単価",
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    # 在庫情報
    stock_quantity = models.PositiveIntegerField("現在庫数", default=0)
    reorder_level = models.PositiveIntegerField("補充閾値", default=0)

    # 詳細情報
    description = models.TextField("備考", blank=True, default="")

    # 画像
    image = models.ImageField("部品画像", upload_to="parts/", blank=True, null=True)

    # 監査情報（作成者・更新者）
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_parts",
        verbose_name="作成者",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="updated_parts",
        verbose_name="更新者",
    )

    # タイムスタンプ
    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    class Meta:
        verbose_name = "部品"
        verbose_name_plural = "部品"
        ordering = ["id"]

    def __str__(self):
        return self.name
