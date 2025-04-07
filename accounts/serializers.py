from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(ModelSerializer):
    """
    ユーザー情報のシリアライザー

    このシリアライザーはユーザー情報の表示のみを目的としており、
    すべてのフィールドが読み取り専用に設定されています。
    ユーザー情報の更新には使用できません。
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
        ]
        read_only_fields = fields  # すべてのフィールドを読み取り専用に設定
