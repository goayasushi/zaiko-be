from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
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
    - 一括削除（POST /api/masters/suppliers/bulk_delete/）
    """

    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]

    @action(methods=["post"], detail=False, url_path="bulk-delete")
    def bulk_delete(self, request):
        """
        複数のサプライヤーを一括で削除する

        リクエストボディに以下の形式でIDリストを含める:
        {
            "ids": [1, 2, 3]
        }

        Returns:
            Response: 削除結果のレスポンス
        """
        ids = request.data.get("ids", [])
        if not ids:
            return Response(
                {"error": "削除対象のIDリストが空です"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 対象のサプライヤーが存在するか確認
        suppliers = Supplier.objects.filter(id__in=ids)
        count_to_delete = suppliers.count()  # 削除前にカウント

        if count_to_delete != len(ids):
            return Response(
                {"error": "指定されたIDの一部が存在しません"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # トランザクションを使用して一括削除
            with transaction.atomic():
                # 削除前に参照整合性チェックなどが必要な場合はここで実装
                suppliers.delete()

            return Response(
                {"message": f"{count_to_delete}件のサプライヤーを削除しました"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"削除中にエラーが発生しました: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
