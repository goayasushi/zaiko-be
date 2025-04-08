from rest_framework import serializers
from masters.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    """
    サプライヤーモデルのシリアライザー

    バリデーションルール：
    - supplier_code: 任意。ユニーク
    - name: 必須
    - phone: 必須
    - email: 必須、有効なメールアドレス形式
    - postal_code: 必須
    - prefecture: 必須
    - city: 必須
    - town: 必須
    """

    class Meta:
        model = Supplier
        fields = "__all__"  # すべてのフィールドを含める

    def validate_supplier_code(self, value):
        """
        supplier_codeが指定されている場合は、ユニークであることを確認
        空文字列の場合はNoneに変換して複数のレコードでの未入力を許可
        """
        # 空文字列の場合はNoneに変換
        if value == "":
            return None

        if value and Supplier.objects.filter(supplier_code=value).exists():
            # 更新時に自分自身のsupplier_codeは除外する
            instance = getattr(self, "instance", None)
            if instance and instance.supplier_code == value:
                return value
            raise serializers.ValidationError(
                "この取引先コードは既に使用されています。"
            )
        return value
