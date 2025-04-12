from django.db import models


class Supplier(models.Model):
    """
    仕入先（サプライヤー）のモデル

    必須項目：
    - name: 仕入先名
    - phone: 電話番号
    - email: メールアドレス
    - postal_code: 郵便番号
    - prefecture: 都道府県
    - city: 市区町村
    - town: 町名・番地
    """

    supplier_code = models.CharField(
        "取引先コード", max_length=50, unique=True, blank=True, null=True
    )
    name = models.CharField("仕入先名", max_length=200)
    contact_person = models.CharField(
        "担当者名", max_length=100, blank=True, default=""
    )
    phone = models.CharField("電話番号", max_length=50)
    fax = models.CharField("FAX番号", max_length=50, blank=True, default="")
    email = models.EmailField("メールアドレス")
    postal_code = models.CharField("郵便番号", max_length=10)
    prefecture = models.CharField("都道府県", max_length=50)
    city = models.CharField("市区町村", max_length=100)
    town = models.CharField("町名・番地", max_length=200)
    building = models.CharField(
        "建物名・部屋番号", max_length=200, blank=True, default=""
    )
    website = models.URLField("Webサイト", blank=True, default="")
    remarks = models.TextField("備考", blank=True, default="")

    created_at = models.DateTimeField("作成日時", auto_now_add=True)
    updated_at = models.DateTimeField("更新日時", auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "仕入先"
        verbose_name_plural = "仕入先"
        ordering = ["created_at"]  # 作成日時順でデフォルト並び替え
