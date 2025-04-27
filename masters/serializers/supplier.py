from rest_framework import serializers
from masters.models import Supplier
from accounts.serializers import UserSerializer


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

    # 作成者と更新者をネストされたオブジェクトとして定義
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Supplier
        fields = "__all__"  # すべてのフィールドを含める
        read_only_fields = ["created_by", "updated_by"]  # 読み取り専用フィールドを指定

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


class SimpleSupplierSerializer(serializers.ModelSerializer):
    """
    サプライヤーの簡易シリアライザー
    ネストされたレスポンスで使用するための最小限のフィールドのみを含む
    """

    class Meta:
        model = Supplier
        fields = ("id", "name")
