from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomUserModelTests(TestCase):
    """カスタムユーザーモデルのテスト"""

    def test_create_user(self):
        """通常ユーザー作成のテスト"""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpassword123",
            first_name="太郎",
            last_name="山田",
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "太郎")
        self.assertEqual(user.last_name, "山田")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)  # usernameがNoneであることを確認

    def test_create_user_without_email(self):
        """メールアドレスなしでユーザー作成を試みるとエラーになるかテスト"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="testpassword123")

    def test_create_superuser(self):
        """スーパーユーザー作成のテスト"""
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword123",
            first_name="管理者",
            last_name="システム",
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertEqual(admin_user.first_name, "管理者")
        self.assertEqual(admin_user.last_name, "システム")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertIsNone(admin_user.username)

    def test_create_superuser_without_is_staff(self):
        """is_staffがFalseのスーパーユーザー作成を試みるとエラーになるかテスト"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com", password="adminpassword123", is_staff=False
            )

    def test_create_superuser_without_is_superuser(self):
        """is_superuserがFalseのスーパーユーザー作成を試みるとエラーになるかテスト"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="admin@example.com",
                password="adminpassword123",
                is_superuser=False,
            )

    def test_user_str_method(self):
        """__str__メソッドが正しく機能するかテスト"""
        user = User.objects.create_user(
            email="test@example.com",
            password="testpassword123",
            first_name="太郎",
            last_name="山田",
        )
        self.assertEqual(str(user), "test@example.com")


class AuthAPITests(APITestCase):
    """認証APIテスト"""

    def setUp(self):
        """テスト用ユーザーの作成"""
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword123",
            first_name="太郎",
            last_name="山田",
        )
        self.client = APIClient()

    def test_login(self):
        """ログインAPIテスト"""
        url = reverse("token_obtain_pair")
        data = {"email": "test@example.com", "password": "testpassword123"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_login_with_wrong_credentials(self):
        """誤った認証情報でのログインテスト"""
        url = reverse("token_obtain_pair")
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_info_authenticated(self):
        """認証済みユーザーのユーザー情報取得テスト"""
        # JWT取得
        refresh = RefreshToken.for_user(self.user)
        access_token = str(refresh.access_token)

        # トークンをヘッダーに設定
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # /info/ エンドポイントにリクエスト
        url = reverse("user_info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")
        self.assertEqual(response.data["first_name"], "太郎")
        self.assertEqual(response.data["last_name"], "山田")
        self.assertTrue(response.data["is_active"])
        self.assertFalse(response.data["is_staff"])
        self.assertFalse(response.data["is_superuser"])

    def test_user_info_unauthenticated(self):
        """未認証ユーザーのユーザー情報取得テスト"""
        # 認証なしで /info/ エンドポイントにリクエスト
        url = reverse("user_info")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "user not authenticated")
