from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import UserSerializer

User = get_user_model()


class UserInfoView(APIView):
    """
    ユーザー情報を取得するAPIビュー
    認証の有無に関わらずアクセス可能だが、認証状態に応じて異なるレスポンスを返す
    """

    permission_classes = [AllowAny]

    def get(self, request):
        # リクエストの認証情報を確認
        if request.user and request.user.is_authenticated:
            # 認証済みの場合、ユーザー情報を返す
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            # 未認証の場合、メッセージを返す
            return Response(
                {"message": "user not authenticated"}, status=status.HTTP_200_OK
            )
