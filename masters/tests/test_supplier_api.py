from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from masters.models import Supplier

User = get_user_model()


class SupplierCreateAPITest(APITestCase):
    """
    サプライヤー作成APIのテストクラス
    """

    def setUp(self):
        """
        テスト前の準備
        """
        # テスト用ユーザーの作成
        self.user = User.objects.create_user(
            email="testuser@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="User",
        )

        # APIクライアントの設定
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # サプライヤー作成用のURL
        self.url = reverse(
            "supplier-list"
        )  # URLパターン名はURLconfでの登録名に合わせる

        # 有効なサプライヤーデータ
        self.valid_supplier_data = {
            "supplier_code": "TEST001",
            "name": "テスト株式会社",
            "contact_person": "テスト太郎",
            "phone": "03-1234-5678",
            "email": "info@test-company.co.jp",
            "postal_code": "100-0001",
            "prefecture": "東京都",
            "city": "千代田区",
            "town": "丸の内1-1-1",
            "building": "テストビル10階",
            "website": "https://www.test-company.co.jp",
            "remarks": "テスト用サプライヤー",
        }

        # 必須フィールドのみのサプライヤーデータ
        self.minimal_supplier_data = {
            "name": "ミニマル株式会社",
            "phone": "03-9876-5432",
            "email": "info@minimal.co.jp",
            "postal_code": "160-0022",
            "prefecture": "東京都",
            "city": "新宿区",
            "town": "新宿3-1-1",
        }

        # 無効なサプライヤーデータ（必須フィールド欠け）
        self.invalid_supplier_data = {
            "supplier_code": "INVALID001",
            "name": "無効データ株式会社",
            # phoneフィールドがない（必須）
            "email": "info@invalid.co.jp",
            # postal_codeフィールドがない（必須）
            "prefecture": "東京都",
            # cityフィールドがない（必須）
            "town": "無効1-1-1",
        }

    def test_create_supplier_with_valid_data(self):
        """
        有効なデータでサプライヤーを作成できるかテスト
        """
        response = self.client.post(self.url, self.valid_supplier_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 1)

        supplier = Supplier.objects.get()
        self.assertEqual(supplier.name, self.valid_supplier_data["name"])
        self.assertEqual(
            supplier.supplier_code, self.valid_supplier_data["supplier_code"]
        )
        self.assertEqual(supplier.phone, self.valid_supplier_data["phone"])
        self.assertEqual(supplier.email, self.valid_supplier_data["email"])

    def test_create_supplier_with_minimal_data(self):
        """
        必須フィールドのみのデータでサプライヤーを作成できるかテスト
        """
        response = self.client.post(self.url, self.minimal_supplier_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 1)

        supplier = Supplier.objects.get()
        self.assertEqual(supplier.name, self.minimal_supplier_data["name"])
        self.assertEqual(supplier.phone, self.minimal_supplier_data["phone"])
        self.assertEqual(
            supplier.supplier_code, None
        )  # supplier_codeは指定していないのでNoneになる

    def test_create_supplier_with_invalid_data(self):
        """
        無効なデータ（必須フィールド欠け）でサプライヤーを作成できないことをテスト
        """
        response = self.client.post(self.url, self.invalid_supplier_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Supplier.objects.count(), 0)  # サプライヤーは作成されない

        # 必須フィールドに関するエラーメッセージが含まれていることを確認
        self.assertIn("phone", response.data)
        self.assertIn("postal_code", response.data)
        self.assertIn("city", response.data)

    def test_create_duplicate_supplier_code(self):
        """
        重複するsupplier_codeでサプライヤーを作成できないことをテスト
        """
        # 最初のサプライヤーを作成
        self.client.post(self.url, self.valid_supplier_data, format="json")

        # 同じsupplier_codeを持つ別のサプライヤーデータ
        duplicate_data = {
            "supplier_code": "TEST001",  # 重複するコード
            "name": "重複コード株式会社",
            "phone": "03-1111-2222",
            "email": "info@duplicate.co.jp",
            "postal_code": "150-0001",
            "prefecture": "東京都",
            "city": "渋谷区",
            "town": "渋谷1-1-1",
        }

        response = self.client.post(self.url, duplicate_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Supplier.objects.count(), 1)  # 最初のサプライヤーだけが存在

        # supplier_codeの一意性に関するエラーメッセージが含まれていることを確認
        self.assertIn("supplier_code", response.data)

    def test_create_supplier_unauthenticated(self):
        """
        未認証ユーザーがサプライヤーを作成できないことをテスト
        """
        # クライアントを未認証状態にする
        self.client.force_authenticate(user=None)

        response = self.client.post(self.url, self.valid_supplier_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Supplier.objects.count(), 0)  # サプライヤーは作成されない
