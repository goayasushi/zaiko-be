from rest_framework import viewsets
from ..models import Part
from ..serializers import PartSerializer
from rest_framework.permissions import IsAuthenticated


class PartViewSet(viewsets.ModelViewSet):
    """
    部品モデルのCRUD操作用ビューセット
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
