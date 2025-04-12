from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    カスタムページネーションクラス

    ページネーションのレスポンスに現在のページ番号と固定のページサイズを追加します。
    """

    page_size = 20  # 固定のページサイズ（20件/ページ）

    def get_paginated_response(self, data):
        """
        ページネーションのレスポンス形式をカスタマイズ
        """
        return Response(
            {
                "count": self.page.paginator.count,  # 総件数
                "total_pages": self.page.paginator.num_pages,  # 総ページ数
                "current": self.page.number,  # 現在のページ番号
                "page_size": self.page_size,  # 固定のページサイズ
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
