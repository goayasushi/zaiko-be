from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from masters.models import Supplier
from masters.serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    """
    サプライヤー情報のCRUD操作を提供するビューセット

    - リスト取得（GET /api/masters/suppliers/）
    - 詳細取得（GET /api/masters/suppliers/{id}/）
    - 新規作成（POST /api/masters/suppliers/）
    - 更新（PUT /api/masters/suppliers/{id}/）
    - 部分更新（PATCH /api/masters/suppliers/{id}/）
    - 削除（DELETE /api/masters/suppliers/{id}/）
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]
