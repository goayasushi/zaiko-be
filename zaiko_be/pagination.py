from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    カスタムページネーションクラス

    ページネーションのレスポンスに現在のページ番号を追加します。
    また、ページサイズをクエリパラメータで変更できるようにします。
    """

    page_size = 20  # デフォルトは20件/ページ

    def get_paginated_response(self, data):
        """
        ページネーションのレスポンス形式をカスタマイズ
        """
        return Response(
            {
                "count": self.page.paginator.count,  # 総件数
                "total_pages": self.page.paginator.num_pages,  # 総ページ数も追加
                "current": self.page.number,  # 現在のページ番号
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
