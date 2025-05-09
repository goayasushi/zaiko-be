from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from ..models import Part
from ..serializers import PartSerializer


class PartViewSet(viewsets.ModelViewSet):
    """
    部品モデルのCRUD操作用ビューセット

    - リスト取得（GET /api/masters/parts/）
    - 詳細取得（GET /api/masters/parts/{id}/）
    - 新規作成（POST /api/masters/parts/）
    - 更新（PUT /api/masters/parts/{id}/）
    - 部分更新（PATCH /api/masters/parts/{id}/）
    - 削除（DELETE /api/masters/parts/{id}/）
    - 一括削除（POST /api/masters/parts/bulk-delete/）
    """

    queryset = Part.objects.select_related("supplier", "created_by", "updated_by").all()
    serializer_class = PartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        新しい部品を作成する際に、現在のユーザーを作成者として設定
        """
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """
        部品を更新する際に、現在のユーザーを更新者として設定
        """
        serializer.save(updated_by=self.request.user)

    @action(methods=["post"], detail=False, url_path="bulk-delete")
    def bulk_delete(self, request):
        """
        複数の部品を一括で削除する

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

        # 対象の部品が存在するか確認
        parts = Part.objects.filter(id__in=ids)
        count_to_delete = parts.count()  # 削除前にカウント

        if count_to_delete != len(ids):
            return Response(
                {"error": "指定されたIDの一部が存在しません"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            # トランザクションを使用して一括削除
            with transaction.atomic():
                # 削除前に参照整合性チェックなどが必要な場合はここで実装
                parts.delete()

            return Response(
                {"message": f"{count_to_delete}件の部品を削除しました"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": f"削除中にエラーが発生しました: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
