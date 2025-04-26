from rest_framework import serializers
from ..models import Part
from accounts.serializers import UserSerializer
from masters.serializers import SupplierSerializer
from masters.models import Supplier


class PartSerializer(serializers.ModelSerializer):
    """
    部品モデル用シリアライザー
    """

    # 作成者と更新者をネストされたオブジェクトとして定義
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    supplier = SupplierSerializer(read_only=True)  # 表示用
    supplier_id = serializers.PrimaryKeyRelatedField(  # 書込用
        queryset=Supplier.objects.all(), source="supplier", write_only=True
    )

    class Meta:
        model = Part
        fields = "__all__"
