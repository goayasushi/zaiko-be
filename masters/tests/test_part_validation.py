from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from masters.serializers import PartSerializer
from masters.models import Supplier

User = get_user_model()


class PartFieldValidationTest(TestCase):
    """
    部品モデルの各フィールドのバリデーションをテストするクラス
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
        self.test_image = SimpleUploadedFile(
            "test_image.png", self.test_image_content, content_type="image/png"
        )

        # 部品作成用のURL
        self.url = reverse("part-list")

        # 有効な部品データ（すべてのテストケースの基準）
        self.valid_part_data = {
            "name": "テスト部品",
            "category": "shaft",
            "supplier_id": self.supplier.id,
            "cost_price": "1000.00",
            "selling_price": "2000.00",
            "stock_quantity": 10,
            "reorder_level": 5,
            "description": "テスト用部品の説明",
            "image": self.test_image,
        }

    def _validate_serializer(self, data):
        """
        シリアライザーを使用してデータを検証し、エラーがあればそれを返す
        """
        serializer = PartSerializer(data=data)
        serializer.is_valid()
        return serializer.errors

    # name フィールドのテスト
    def test_name_required(self):
        """
        nameが必須であることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data.pop("name")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("name", errors)
        self.assertIn("この項目は必須です", str(errors["name"]))

    def test_name_empty_string(self):
        """
        nameが空文字の場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["name"] = ""

        errors = self._validate_serializer(invalid_data)
        self.assertIn("name", errors)
        self.assertIn("この項目は空にできません", str(errors["name"]))

    def test_name_boundary_values(self):
        """
        名前フィールドの境界値テスト
        境界値-1（199文字）、境界値（200文字）、境界値+1（201文字）の場合をテスト
        """
        # 境界値-1（199文字）: 有効
        data_199 = self.valid_part_data.copy()
        data_199["name"] = "あ" * 199
        errors = self._validate_serializer(data_199)
        self.assertNotIn("name", errors)

        # 境界値（200文字）: 有効
        data_200 = self.valid_part_data.copy()
        data_200["name"] = "あ" * 200
        errors = self._validate_serializer(data_200)
        self.assertNotIn("name", errors)

        # 境界値+1（201文字）: 無効
        data_201 = self.valid_part_data.copy()
        data_201["name"] = "あ" * 201
        errors = self._validate_serializer(data_201)
        self.assertIn("name", errors)
        self.assertIn("max_length", str(errors["name"]))

    # category フィールドのテスト
    def test_category_required(self):
        """
        categoryが必須であることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data.pop("category")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("category", errors)
        self.assertIn("この項目は必須です", str(errors["category"]))

    def test_category_empty_string(self):
        """
        categoryが空文字の場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["category"] = ""

        errors = self._validate_serializer(invalid_data)
        self.assertIn("category", errors)
        self.assertIn("有効な選択肢ではありません", str(errors["category"]))

    def test_category_invalid_choice(self):
        """
        categoryが有効な選択肢でない場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["category"] = "invalid_category"

        errors = self._validate_serializer(invalid_data)
        self.assertIn("category", errors)
        self.assertIn("有効な選択肢ではありません", str(errors["category"]))

    def test_category_valid_choices(self):
        """
        categoryが有効な選択肢の場合エラーにならないことをテスト
        """
        valid_choices = ["head", "shaft", "grip", "other"]

        for choice in valid_choices:
            valid_data = self.valid_part_data.copy()
            valid_data["category"] = choice

            errors = self._validate_serializer(valid_data)
            self.assertNotIn("category", errors)

    # supplier_id フィールドのテスト
    def test_supplier_id_required(self):
        """
        supplier_idが必須であることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data.pop("supplier_id")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("supplier_id", errors)
        self.assertIn("この項目は必須です", str(errors["supplier_id"]))

    def test_supplier_id_invalid(self):
        """
        存在しないsupplier_idの場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["supplier_id"] = 999999  # 存在しないID

        errors = self._validate_serializer(invalid_data)
        self.assertIn("supplier_id", errors)
        self.assertIn("データが存在しません", str(errors["supplier_id"]))

    # cost_price フィールドのテスト
    def test_cost_price_required(self):
        """
        cost_priceが必須であることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data.pop("cost_price")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("cost_price", errors)
        self.assertIn("この項目は必須です", str(errors["cost_price"]))

    def test_cost_price_negative(self):
        """
        cost_priceが負の値の場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["cost_price"] = "-100.00"

        errors = self._validate_serializer(invalid_data)
        self.assertIn("cost_price", errors)
        self.assertIn("0.00以上", str(errors["cost_price"]))

    def test_cost_price_format(self):
        """
        cost_priceが数値として無効な場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["cost_price"] = "invalid_price"

        errors = self._validate_serializer(invalid_data)
        self.assertIn("cost_price", errors)
        self.assertIn("数値", str(errors["cost_price"]))

    # selling_price フィールドのテスト
    def test_selling_price_required(self):
        """
        selling_priceが必須であることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data.pop("selling_price")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("selling_price", errors)
        self.assertIn("この項目は必須です", str(errors["selling_price"]))

    def test_selling_price_negative(self):
        """
        selling_priceが負の値の場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["selling_price"] = "-100.00"

        errors = self._validate_serializer(invalid_data)
        self.assertIn("selling_price", errors)
        self.assertIn("0.00以上", str(errors["selling_price"]))

    def test_selling_price_format(self):
        """
        selling_priceが数値として無効な場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["selling_price"] = "invalid_price"

        errors = self._validate_serializer(invalid_data)
        self.assertIn("selling_price", errors)
        self.assertIn("数値", str(errors["selling_price"]))

    # stock_quantity フィールドのテスト
    def test_stock_quantity_negative(self):
        """
        stock_quantityが負の値の場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["stock_quantity"] = -10

        errors = self._validate_serializer(invalid_data)
        self.assertIn("stock_quantity", errors)
        self.assertIn("0以上", str(errors["stock_quantity"]))

    def test_stock_quantity_non_integer(self):
        """
        stock_quantityが整数でない場合エラーになることをテスト
        """
        # 文字列を渡す場合
        invalid_string_data = self.valid_part_data.copy()
        invalid_string_data["stock_quantity"] = "十個"

        errors = self._validate_serializer(invalid_string_data)
        self.assertIn("stock_quantity", errors)
        self.assertIn("有効な整数", str(errors["stock_quantity"]))

        # 浮動小数点数を渡す場合
        invalid_float_data = self.valid_part_data.copy()
        invalid_float_data["stock_quantity"] = 10.5

        errors = self._validate_serializer(invalid_float_data)
        self.assertIn("stock_quantity", errors)
        self.assertIn("整数", str(errors["stock_quantity"]))

    # reorder_level フィールドのテスト
    def test_reorder_level_negative(self):
        """
        reorder_levelが負の値の場合エラーになることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data["reorder_level"] = -5

        errors = self._validate_serializer(invalid_data)
        self.assertIn("reorder_level", errors)
        self.assertIn("0以上", str(errors["reorder_level"]))

    def test_reorder_level_non_integer(self):
        """
        reorder_levelが整数でない場合エラーになることをテスト
        """
        # 文字列を渡す場合
        invalid_string_data = self.valid_part_data.copy()
        invalid_string_data["reorder_level"] = "五個"

        errors = self._validate_serializer(invalid_string_data)
        self.assertIn("reorder_level", errors)
        self.assertIn("有効な整数", str(errors["reorder_level"]))

        # 浮動小数点数を渡す場合
        invalid_float_data = self.valid_part_data.copy()
        invalid_float_data["reorder_level"] = 5.5

        errors = self._validate_serializer(invalid_float_data)
        self.assertIn("reorder_level", errors)
        self.assertIn("整数", str(errors["reorder_level"]))

    # image フィールドのテスト
    def test_image_invalid_format(self):
        """
        無効な画像フォーマットではエラーになることをテスト
        """
        # 無効なファイル（画像でないテキストファイル）
        invalid_file = SimpleUploadedFile(
            "test.txt", b"This is not an image file.", content_type="text/plain"
        )

        data_with_invalid_file = self.valid_part_data.copy()
        data_with_invalid_file["image"] = invalid_file

        errors = self._validate_serializer(data_with_invalid_file)
        self.assertIn("image", errors)
        self.assertIn(
            "画像", str(errors["image"])
        )  # "有効な画像"などのメッセージが含まれているか

    # 複数フィールドの組み合わせテスト
    def test_multiple_validation_errors(self):
        """
        複数のフィールドが同時に無効な場合、すべてのエラーが返されることをテスト
        """
        invalid_data = self.valid_part_data.copy()
        invalid_data.pop("name")  # 必須フィールドを削除
        invalid_data["category"] = "invalid_category"  # 無効なカテゴリ
        invalid_data["cost_price"] = "-100.00"  # 負の原価

        errors = self._validate_serializer(invalid_data)
        self.assertIn("name", errors)
        self.assertIn("category", errors)
        self.assertIn("cost_price", errors)

    # 正常系のテスト
    def test_valid_data(self):
        """
        有効なデータでエラーが発生しないことをテスト
        """
        errors = self._validate_serializer(self.valid_part_data)
        self.assertEqual(len(errors), 0)

    def test_valid_minimal_data(self):
        """
        必須フィールドのみの最小限のデータでエラーが発生しないことをテスト
        """
        minimal_data = {
            "name": "最小限テスト部品",
            "category": "other",
            "supplier_id": self.supplier.id,
            "cost_price": "500.00",
            "selling_price": "1000.00",
        }

        errors = self._validate_serializer(minimal_data)
        self.assertEqual(len(errors), 0)
