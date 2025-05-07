from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from masters.models import Supplier, Part
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
import os

User = get_user_model()


class PartCreateAPITest(APITestCase):
    """
    部品作成APIのテストクラス
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

        # テスト用サプライヤーの作成
        self.supplier = Supplier.objects.create(
            name="テストサプライヤー",
            phone="03-1234-5678",
            email="supplier@example.com",
            postal_code="100-0001",
            prefecture="東京都",
            city="千代田区",
            town="丸の内1-1-1",
        )

        # テスト用の小さな画像を作成
        self.test_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"

        # 部品作成用のURL
        self.url = reverse("part-list")

        # 有効な部品データ
        self.valid_part_data = {
            "name": "テスト部品",
            "category": "shaft",
            "supplier_id": self.supplier.id,
            "cost_price": "1000.00",
            "selling_price": "2000.00",
            "tax_rate": "10.00",
            "stock_quantity": 10,
            "reorder_level": 5,
            "description": "テスト用部品の説明",
            # imageフィールドは個別のテストで扱います
        }

        # 必須フィールドのみの部品データ
        self.minimal_part_data = {
            "name": "最小限テスト部品",
            "category": "other",
            "supplier_id": self.supplier.id,
            "cost_price": "500.00",
            "selling_price": "1000.00",
        }

        # 無効な部品データ（必須フィールド欠け）
        self.invalid_part_data = {
            "name": "無効データ部品",
            # categoryフィールドがない（必須）
            "supplier_id": self.supplier.id,
            # cost_priceフィールドがない（必須）
            # selling_priceフィールドがない（必須）
            "stock_quantity": 5,
        }

    def test_create_part_with_valid_data(self):
        """
        有効なデータで部品を作成できるかテスト
        """
        response = self.client.post(self.url, self.valid_part_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Part.objects.count(), 1)

        part = Part.objects.get()
        self.assertEqual(part.name, self.valid_part_data["name"])
        self.assertEqual(part.category, self.valid_part_data["category"])
        self.assertEqual(part.supplier.id, self.valid_part_data["supplier_id"])
        self.assertEqual(part.cost_price, Decimal(self.valid_part_data["cost_price"]))
        self.assertEqual(
            part.selling_price, Decimal(self.valid_part_data["selling_price"])
        )
        self.assertEqual(part.tax_rate, Decimal(self.valid_part_data["tax_rate"]))
        self.assertEqual(part.stock_quantity, self.valid_part_data["stock_quantity"])
        self.assertEqual(part.reorder_level, self.valid_part_data["reorder_level"])
        self.assertEqual(part.description, self.valid_part_data["description"])

        # 作成者と更新者が現在のユーザーに設定されていることを確認
        self.assertEqual(part.created_by, self.user)
        self.assertEqual(part.updated_by, self.user)

    def test_create_part_with_minimal_data(self):
        """
        必須フィールドのみのデータで部品を作成できるかテスト
        """
        response = self.client.post(self.url, self.minimal_part_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Part.objects.count(), 1)

        part = Part.objects.get()
        self.assertEqual(part.name, self.minimal_part_data["name"])
        self.assertEqual(part.category, self.minimal_part_data["category"])
        self.assertEqual(part.supplier.id, self.minimal_part_data["supplier_id"])
        self.assertEqual(part.cost_price, Decimal(self.minimal_part_data["cost_price"]))
        self.assertEqual(
            part.selling_price, Decimal(self.minimal_part_data["selling_price"])
        )
        self.assertEqual(part.tax_rate, Decimal("10.00"))  # デフォルト値
        self.assertEqual(part.stock_quantity, 0)  # デフォルト値
        self.assertEqual(part.reorder_level, 0)  # デフォルト値
        self.assertEqual(part.description, "")  # デフォルト値

        # 作成者と更新者が現在のユーザーに設定されていることを確認
        self.assertEqual(part.created_by, self.user)
        self.assertEqual(part.updated_by, self.user)

    def test_create_part_with_empty_tax_rate(self):
        """
        空の税率を送信した場合にデフォルト値が適用されるかテスト
        """
        data_with_empty_tax = self.valid_part_data.copy()
        data_with_empty_tax["tax_rate"] = ""  # 空の税率

        response = self.client.post(self.url, data_with_empty_tax, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Part.objects.count(), 1)

        part = Part.objects.get()
        self.assertEqual(part.tax_rate, Decimal("10.00"))  # デフォルト値が適用される

    def test_create_part_with_empty_string_values(self):
        """
        stock_quantityとreorder_levelに空文字列を設定しても正しく0に変換されることをテスト
        """
        data_with_empty_strings = self.valid_part_data.copy()
        data_with_empty_strings["stock_quantity"] = ""
        data_with_empty_strings["reorder_level"] = ""

        response = self.client.post(self.url, data_with_empty_strings, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Part.objects.count(), 1)

        part = Part.objects.get()
        # 空文字列が0に正しく変換されていることを確認
        self.assertEqual(part.stock_quantity, 0)
        self.assertEqual(part.reorder_level, 0)

    def test_create_part_with_invalid_data(self):
        """
        無効なデータ（必須フィールド欠け）で部品を作成できないことをテスト
        """
        response = self.client.post(self.url, self.invalid_part_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Part.objects.count(), 0)  # 部品は作成されない

        # 必須フィールドに関するエラーメッセージが含まれていることを確認
        self.assertIn("category", response.data)
        self.assertIn("cost_price", response.data)
        self.assertIn("selling_price", response.data)

    def test_create_part_with_invalid_supplier(self):
        """
        存在しないサプライヤーIDで部品を作成できないことをテスト
        """
        invalid_supplier_data = self.valid_part_data.copy()
        invalid_supplier_data["supplier_id"] = 999999  # 存在しないID

        response = self.client.post(self.url, invalid_supplier_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Part.objects.count(), 0)  # 部品は作成されない

        # サプライヤーIDに関するエラーメッセージが含まれていることを確認
        self.assertIn("supplier_id", response.data)

    def test_create_part_with_negative_prices(self):
        """
        負の価格値で部品を作成できないことをテスト
        """
        invalid_price_data = self.valid_part_data.copy()
        invalid_price_data["cost_price"] = "-100.00"
        invalid_price_data["selling_price"] = "-200.00"

        response = self.client.post(self.url, invalid_price_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Part.objects.count(), 0)  # 部品は作成されない

        # 価格フィールドに関するエラーメッセージが含まれていることを確認
        self.assertIn("cost_price", response.data)
        self.assertIn("selling_price", response.data)

    def test_create_part_with_invalid_category(self):
        """
        無効なカテゴリで部品を作成できないことをテスト
        """
        invalid_category_data = self.valid_part_data.copy()
        invalid_category_data["category"] = "invalid_category"

        response = self.client.post(self.url, invalid_category_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Part.objects.count(), 0)  # 部品は作成されない

        # カテゴリフィールドに関するエラーメッセージが含まれていることを確認
        self.assertIn("category", response.data)

    def test_create_part_unauthenticated(self):
        """
        未認証ユーザーが部品を作成できないことをテスト
        """
        # クライアントを未認証状態にする
        self.client.force_authenticate(user=None)

        response = self.client.post(self.url, self.valid_part_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Part.objects.count(), 0)  # 部品は作成されない

    def test_create_part_with_image(self):
        """
        画像付きで部品を作成できることをテスト
        """
        # 画像を含むデータを準備（テスト毎に新しいSimpleUploadFileを作成）
        test_image = SimpleUploadedFile(
            "test_image.png", self.test_image_content, content_type="image/png"
        )

        # APIクライアントでPOSTリクエストを送信
        # マルチパートフォームデータとして送信（画像を含むため）
        response = self.client.post(
            self.url,
            data={**self.valid_part_data, "image": test_image},
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 作成された部品を取得して確認
        part = Part.objects.get()
        self.assertEqual(part.name, self.valid_part_data["name"])

        # 画像が保存されていることを確認
        self.assertTrue(part.image)
        self.assertTrue(os.path.exists(part.image.path))

        # テスト後にアップロードされた画像ファイルを削除
        if part.image and os.path.exists(part.image.path):
            os.remove(part.image.path)

    def test_create_part_with_invalid_image(self):
        """
        無効な画像でエラーになることをテスト
        """
        # 無効なファイル（画像でないテキストファイル）
        invalid_file = SimpleUploadedFile(
            "invalid.txt", b"This is not an image file.", content_type="text/plain"
        )

        # 無効な画像を含むデータを準備
        data_with_invalid_image = self.valid_part_data.copy()

        # APIクライアントでPOSTリクエストを送信
        response = self.client.post(
            self.url,
            data={**data_with_invalid_image, "image": invalid_file},
            format="multipart",
        )

        # 検証
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("image", response.data)
        self.assertEqual(Part.objects.count(), 0)  # 部品は作成されない


class PartListAPITest(APITestCase):
    """
    部品一覧取得APIのテストクラス
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

        # 部品一覧取得用のURL
        self.url = reverse("part-list")

        # テスト用サプライヤーの作成
        self.supplier1 = Supplier.objects.create(
            name="サプライヤーA",
            phone="03-1234-5678",
            email="supplierA@example.com",
            postal_code="100-0001",
            prefecture="東京都",
            city="千代田区",
            town="丸の内1-1-1",
        )

        self.supplier2 = Supplier.objects.create(
            name="サプライヤーB",
            phone="03-8765-4321",
            email="supplierB@example.com",
            postal_code="160-0022",
            prefecture="東京都",
            city="新宿区",
            town="新宿3-1-1",
        )

        # テスト用部品データの作成
        self.parts = []
        categories = [
            Part.Category.SHAFT,
            Part.Category.HEAD,
            Part.Category.GRIP,
            Part.Category.OTHER,
            Part.Category.OTHER,
        ]

        for i in range(5):
            part = Part.objects.create(
                name=f"テスト部品{i}",
                category=categories[i].value,
                supplier=self.supplier1 if i % 2 == 0 else self.supplier2,
                cost_price=Decimal(f"{1000 + i * 100}.00"),
                selling_price=Decimal(f"{2000 + i * 200}.00"),
                tax_rate=Decimal("10.00"),
                stock_quantity=10 + i * 5,
                reorder_level=5 + i,
                description=(
                    f"テスト用部品{i}の説明" if i != 0 else ""
                ),  # 説明なしのケースも含める
                created_by=self.user,
                updated_by=self.user,
            )
            self.parts.append(part)

    def test_list_parts(self):
        """
        部品一覧を取得できることをテスト
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

    def test_list_parts_pagination(self):
        """
        ページネーションが正しく機能していることをテスト
        - 合計30件の部品データを作成し、ページネーションが機能するか確認
        """
        # さらに25件の部品を追加（合計30件）
        for i in range(5, 30):
            Part.objects.create(
                name=f"追加部品{i}",
                category=Part.Category.OTHER.value,
                supplier=self.supplier1 if i % 2 == 0 else self.supplier2,
                cost_price=Decimal(f"{500 + i * 50}.00"),
                selling_price=Decimal(f"{1000 + i * 100}.00"),
                tax_rate=Decimal("10.00"),
                stock_quantity=i,
                reorder_level=i // 2,
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
        # さらに25件の部品を追加（合計30件）
        for i in range(5, 30):
            Part.objects.create(
                name=f"追加部品{i}",
                category=Part.Category.OTHER.value,
                supplier=self.supplier1 if i % 2 == 0 else self.supplier2,
                cost_price=Decimal(f"{500 + i * 50}.00"),
                selling_price=Decimal(f"{1000 + i * 100}.00"),
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

    def test_list_parts_unauthenticated(self):
        """
        未認証ユーザーが部品一覧を取得できないことをテスト
        """
        # クライアントを未認証状態にする
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_parts_fields(self):
        """
        部品一覧の各フィールドが正しく取得できることをテスト
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # レスポンスデータを取得
        if "results" in response.data:
            parts_data = response.data["results"]
        else:
            parts_data = response.data

        # 1件目の部品データを検証
        part_data = next((p for p in parts_data if p["name"] == "テスト部品0"), None)
        self.assertIsNotNone(part_data)

        # 各フィールドが正しく含まれていることを確認
        self.assertEqual(part_data["name"], "テスト部品0")
        self.assertEqual(part_data["category"], Part.Category.SHAFT.value)
        self.assertEqual(part_data["supplier"]["id"], self.supplier1.id)
        self.assertEqual(part_data["supplier"]["name"], self.supplier1.name)
        self.assertEqual(part_data["cost_price"], "1000.00")
        self.assertEqual(part_data["selling_price"], "2000.00")
        self.assertEqual(part_data["tax_rate"], "10.00")
        self.assertEqual(part_data["stock_quantity"], 10)
        self.assertEqual(part_data["reorder_level"], 5)
        self.assertEqual(part_data["description"], "")  # 0番目は説明なし

        # 作成者・更新者情報が含まれていることを確認
        self.assertIn("created_by", part_data)
        self.assertIn("updated_by", part_data)

    def test_list_parts_supplier_nested_data(self):
        """
        部品一覧でサプライヤー情報がネストされて返されることをテスト
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # レスポンスデータを取得
        if "results" in response.data:
            parts_data = response.data["results"]
        else:
            parts_data = response.data

        # サプライヤーBが設定された部品を検証
        part_with_supplier_b = next(
            (p for p in parts_data if p["supplier"]["id"] == self.supplier2.id), None
        )
        self.assertIsNotNone(part_with_supplier_b)

        # サプライヤー情報がネストされていることを確認
        self.assertEqual(part_with_supplier_b["supplier"]["id"], self.supplier2.id)
        self.assertEqual(part_with_supplier_b["supplier"]["name"], "サプライヤーB")

    def test_list_parts_empty(self):
        """
        部品が1件も登録されていない場合の挙動をテスト
        """
        # すべての部品を削除
        Part.objects.all().delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ページネーションありの場合
        if "results" in response.data:
            self.assertEqual(response.data["count"], 0)
            self.assertEqual(len(response.data["results"]), 0)
        else:
            # ページネーションなしの場合
            self.assertEqual(len(response.data), 0)
