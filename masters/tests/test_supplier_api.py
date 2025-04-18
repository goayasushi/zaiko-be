from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from masters.models import Supplier
from unittest.mock import patch

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


class SupplierListAPITest(APITestCase):
    """
    サプライヤー一覧取得APIのテストクラス
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

        # サプライヤー一覧取得用のURL
        self.url = reverse("supplier-list")

        # テスト用サプライヤーデータの作成
        self.suppliers = []
        for i in range(5):
            supplier = Supplier.objects.create(
                supplier_code=(
                    f"CODE{i:03d}" if i != 2 else None
                ),  # コードなしのケースも含める
                name=f"テスト株式会社{i}",
                contact_person=(
                    f"担当者{i}" if i != 3 else ""
                ),  # 担当者なしのケースも含める
                phone=f"03-1234-{i:04d}",
                email=f"test{i}@example.com",
                postal_code=f"100-{i:04d}",
                prefecture="東京都",
                city="千代田区",
                town=f"丸の内{i}-{i}-{i}",
                building=f"ビル{i}階" if i != 4 else "",  # 建物なしのケースも含める
                website=(
                    f"https://test{i}.com" if i != 1 else ""
                ),  # Webサイトなしのケースも含める
                remarks=f"備考{i}" if i != 0 else "",  # 備考なしのケースも含める
            )
            self.suppliers.append(supplier)

    def test_list_suppliers(self):
        """
        サプライヤー一覧を取得できることをテスト
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ページネーションが適用されている場合
        if "results" in response.data:
            result_data = response.data["results"]
            self.assertEqual(len(result_data), 5)  # テストで作成した5件のデータ
        else:
            # ページネーションが適用されていない場合
            self.assertEqual(len(response.data), 5)  # テストで作成した5件のデータ

    def test_list_suppliers_pagination(self):
        """
        ページネーションが正しく機能していることをテスト
        - 合計30件のサプライヤーデータを作成し、ページネーションが機能するか確認
        """
        # さらに25件のサプライヤーを追加（合計30件）
        for i in range(5, 30):
            Supplier.objects.create(
                name=f"追加株式会社{i}",
                phone=f"03-5678-{i:04d}",
                email=f"add{i}@example.com",
                postal_code=f"160-{i:04d}",
                prefecture="大阪府",
                city="大阪市",
                town=f"梅田{i}-{i}",
            )

        # 1ページ目を取得
        response = self.client.get(f"{self.url}?page=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ページネーションのレスポンス構造を確認
        self.assertIn("count", response.data)
        self.assertEqual(response.data["count"], 30)  # 合計30件

        # ページネーション設定（20件/ページ）が反映されているか確認
        self.assertEqual(len(response.data["results"]), 20)

        # 2ページ目を取得して残りのデータがあることを確認
        response2 = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response2.data["results"]), 10)  # 残り10件

    def test_custom_pagination_format(self):
        """
        カスタムページネーションのレスポンス形式をテスト
        - 'current', 'total_pages', 'page_size'などのカスタムフィールドが含まれているか確認
        """
        # さらに25件のサプライヤーを追加（合計30件）
        for i in range(5, 30):
            Supplier.objects.create(
                name=f"追加株式会社{i}",
                phone=f"03-5678-{i:04d}",
                email=f"add{i}@example.com",
                postal_code=f"160-{i:04d}",
                prefecture="大阪府",
                city="大阪市",
                town=f"梅田{i}-{i}",
            )

        # APIレスポンスを取得
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # カスタムページネーション形式のフィールドをチェック
        self.assertIn("count", response.data)
        self.assertIn("results", response.data)

        # カスタムフィールドの存在確認
        self.assertIn("current", response.data)
        self.assertIn("total_pages", response.data)
        self.assertIn("page_size", response.data)  # ページサイズフィールドの存在確認
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

        # 値の検証
        self.assertEqual(response.data["current"], 1)  # 現在のページは1
        self.assertEqual(response.data["total_pages"], 2)  # 30件なので2ページ
        self.assertEqual(response.data["page_size"], 20)  # ページサイズは常に20

        # ページ2に移動して検証
        response2 = self.client.get(f"{self.url}?page=2")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(response2.data["current"], 2)  # 現在のページは2
        self.assertEqual(response2.data["total_pages"], 2)  # 総ページ数は変わらず2
        self.assertEqual(response2.data["page_size"], 20)  # ページサイズは常に20

    def test_list_suppliers_unauthenticated(self):
        """
        未認証ユーザーがサプライヤー一覧を取得できないことをテスト
        """
        # クライアントを未認証状態にする
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_suppliers_fields(self):
        """
        サプライヤー一覧の各フィールドが正しく取得できることをテスト
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # レスポンスデータを取得
        if "results" in response.data:
            suppliers_data = response.data["results"]
        else:
            suppliers_data = response.data

        # 1件目のサプライヤーデータを検証
        supplier_data = next(
            (s for s in suppliers_data if s["name"] == "テスト株式会社0"), None
        )
        self.assertIsNotNone(supplier_data)

        # 各フィールドが正しく含まれていることを確認
        self.assertEqual(supplier_data["supplier_code"], "CODE000")
        self.assertEqual(supplier_data["name"], "テスト株式会社0")
        self.assertEqual(supplier_data["contact_person"], "担当者0")
        self.assertEqual(supplier_data["phone"], "03-1234-0000")
        self.assertEqual(supplier_data["email"], "test0@example.com")
        self.assertEqual(supplier_data["prefecture"], "東京都")
        self.assertEqual(supplier_data["city"], "千代田区")
        self.assertEqual(supplier_data["town"], "丸の内0-0-0")
        self.assertEqual(supplier_data["building"], "ビル0階")
        self.assertEqual(supplier_data["website"], "https://test0.com")
        self.assertEqual(supplier_data["remarks"], "")  # 0番目は備考なし

    def test_list_suppliers_empty(self):
        """
        サプライヤーが1件も登録されていない場合の挙動をテスト
        """
        # すべてのサプライヤーを削除
        Supplier.objects.all().delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ページネーションありの場合
        if "results" in response.data:
            self.assertEqual(response.data["count"], 0)
            self.assertEqual(len(response.data["results"]), 0)
        else:
            # ページネーションなしの場合
            self.assertEqual(len(response.data), 0)


class SupplierBulkDeleteAPITest(APITestCase):
    """サプライヤー一括削除のテスト"""

    def setUp(self):
        # テストユーザーの作成とログイン
        self.user = User.objects.create_user(
            email="test@example.com",
            password="password",
            first_name="テスト",
            last_name="ユーザー",
        )
        self.client.force_authenticate(user=self.user)

        # テスト用サプライヤーデータの作成
        self.suppliers = []
        for i in range(5):
            supplier = Supplier.objects.create(
                name=f"テストサプライヤー{i}",
                phone=f"0123456789{i}",
                email=f"supplier{i}@example.com",
                postal_code="123-4567",
                prefecture="東京都",
                city="千代田区",
                town="丸の内1-1-1",
            )
            self.suppliers.append(supplier)

        # 一括削除のエンドポイントURL
        self.bulk_delete_url = reverse("supplier-bulk-delete")

    def test_bulk_delete_success(self):
        """複数のサプライヤーを正常に削除できることを確認"""
        # 削除対象のID
        ids = [self.suppliers[0].id, self.suppliers[1].id]
        count_to_delete = len(ids)  # 削除対象の件数

        # リクエスト実行
        response = self.client.post(
            self.bulk_delete_url, data={"ids": ids}, format="json"
        )

        # レスポンス確認
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)
        self.assertIn(
            f"{count_to_delete}件", response.data["message"]
        )  # 正確な件数が含まれているか確認

        # DBから削除されたことを確認
        for supplier_id in ids:
            self.assertFalse(Supplier.objects.filter(id=supplier_id).exists())

        # 他のサプライヤーが削除されていないことを確認
        self.assertEqual(Supplier.objects.count(), 3)

    def test_bulk_delete_empty_ids(self):
        """空のIDリストでエラーが返されることを確認"""
        # 空のIDリストで削除を実行
        response = self.client.post(
            self.bulk_delete_url, data={"ids": []}, format="json"
        )

        # レスポンス確認
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

        # DBのレコード数が変わっていないことを確認
        self.assertEqual(Supplier.objects.count(), 5)

    def test_bulk_delete_nonexistent_ids(self):
        """存在しないIDを含む場合、エラーが返されることを確認"""
        # 存在しないIDを含む削除リスト
        max_id = Supplier.objects.order_by("-id").first().id
        ids = [self.suppliers[0].id, max_id + 100]

        # リクエスト実行
        response = self.client.post(
            self.bulk_delete_url, data={"ids": ids}, format="json"
        )

        # レスポンス確認
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

        # DBのレコード数が変わっていないことを確認
        self.assertEqual(Supplier.objects.count(), 5)

    def test_bulk_delete_unauthorized(self):
        """未認証ユーザーはアクセスできないことを確認"""
        # クライアントからの認証を削除
        self.client.force_authenticate(user=None)

        # 削除対象のID
        ids = [self.suppliers[0].id, self.suppliers[1].id]

        # リクエスト実行
        response = self.client.post(
            self.bulk_delete_url, data={"ids": ids}, format="json"
        )

        # 認証エラーになることを確認
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # DBのレコード数が変わっていないことを確認
        self.assertEqual(Supplier.objects.count(), 5)

    def test_bulk_delete_transaction_error(self):
        """トランザクションエラー時の処理をテスト"""
        # 削除対象のID
        ids = [self.suppliers[0].id, self.suppliers[1].id]

        # Supplier.delete()メソッドでエラーを発生させるようにモック
        with patch("django.db.models.query.QuerySet.delete") as mock_delete:
            # delete()呼び出し時に例外をスロー
            mock_delete.side_effect = Exception("テスト用の強制エラー")

            # リクエスト実行
            response = self.client.post(
                self.bulk_delete_url, data={"ids": ids}, format="json"
            )

            # レスポンスの検証
            self.assertEqual(
                response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            self.assertIn("error", response.data)
            self.assertIn("テスト用の強制エラー", response.data["error"])

        # データベースのレコードが削除されていないことを確認
        self.assertEqual(Supplier.objects.count(), 5)


class SupplierRetrieveAPITest(APITestCase):
    """
    サプライヤー詳細取得APIのテストクラス
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

        # テスト用サプライヤーデータの作成
        self.supplier = Supplier.objects.create(
            supplier_code="TEST123",
            name="テスト詳細株式会社",
            contact_person="詳細テスト太郎",
            phone="03-1234-5678",
            email="detail@example.com",
            postal_code="100-0001",
            prefecture="東京都",
            city="千代田区",
            town="丸の内1-1-1",
            building="詳細ビル10階",
            website="https://www.detail-test.co.jp",
            remarks="詳細取得テスト用データ",
        )

        # サプライヤー詳細取得用のURL
        self.url = reverse("supplier-detail", args=[self.supplier.id])

    def test_retrieve_supplier(self):
        """
        サプライヤー詳細を取得できることをテスト
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 各フィールドの値が正しく取得できることを確認
        self.assertEqual(response.data["id"], self.supplier.id)
        self.assertEqual(response.data["supplier_code"], self.supplier.supplier_code)
        self.assertEqual(response.data["name"], self.supplier.name)
        self.assertEqual(response.data["contact_person"], self.supplier.contact_person)
        self.assertEqual(response.data["phone"], self.supplier.phone)
        self.assertEqual(response.data["email"], self.supplier.email)
        self.assertEqual(response.data["postal_code"], self.supplier.postal_code)
        self.assertEqual(response.data["prefecture"], self.supplier.prefecture)
        self.assertEqual(response.data["city"], self.supplier.city)
        self.assertEqual(response.data["town"], self.supplier.town)
        self.assertEqual(response.data["building"], self.supplier.building)
        self.assertEqual(response.data["website"], self.supplier.website)
        self.assertEqual(response.data["remarks"], self.supplier.remarks)

    def test_retrieve_nonexistent_supplier(self):
        """
        存在しないIDのサプライヤー詳細を取得しようとすると404が返ることをテスト
        """
        # 存在しないIDのURL
        nonexistent_url = reverse("supplier-detail", args=[999999])

        response = self.client.get(nonexistent_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve_supplier_unauthenticated(self):
        """
        未認証ユーザーがサプライヤー詳細を取得できないことをテスト
        """
        # クライアントを未認証状態にする
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
