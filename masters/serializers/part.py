from rest_framework import serializers
from ..models import Part, Supplier
from accounts.serializers import UserSerializer
from .supplier import SimpleSupplierSerializer


class PartSerializer(serializers.ModelSerializer):
    """
    部品モデル用シリアライザー
    """

    # 仕入先は簡易シリアライザーでネストし、作成時の外部キー参照はsupplier_idで受け取る
    supplier = SimpleSupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), source="supplier", write_only=True
    )
    # 作成者と更新者をネストされたオブジェクトとして定義
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = Part
        fields = "__all__"

    def to_internal_value(self, data):
        """
        空文字列の数値フィールドをデフォルト値に変換
        stock_quantityとreorder_levelフィールドに空文字列が送られた場合、0に変換
        """
        data = data.copy()
        for field in ["stock_quantity", "reorder_level"]:
            if data.get(field, None) == "":
                data[field] = 0
        return super().to_internal_value(data)
