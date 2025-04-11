from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse

from masters.serializers import SupplierSerializer

User = get_user_model()


class SupplierFieldValidationTest(TestCase):
    """
    サプライヤーモデルの各フィールドのバリデーションをテストするクラス
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
        self.url = reverse("supplier-list")

        # 有効なサプライヤーデータ（すべてのテストケースの基準）
        self.valid_supplier_data = {
            "supplier_code": "TEST001",
            "name": "テスト株式会社",
            "contact_person": "テスト太郎",
            "phone": "03-1234-5678",
            "fax": "03-1234-5679",
            "email": "info@test.co.jp",
            "postal_code": "100-0001",
            "prefecture": "東京都",
            "city": "千代田区",
            "town": "丸の内1-1-1",
            "building": "テストビル10階",
            "website": "https://www.test.co.jp",
            "remarks": "テスト用サプライヤー",
        }

    def _validate_serializer(self, data):
        """
        シリアライザーを使用してデータを検証し、エラーがあればそれを返す
        """
        serializer = SupplierSerializer(data=data)
        serializer.is_valid()
        return serializer.errors

    # supplier_code フィールドのテスト
    def test_supplier_code_boundary_values(self):
        """
        supplier_codeフィールドの境界値テスト
        境界値-1（49文字）、境界値（50文字）、境界値+1（51文字）の場合をテスト
        """
        # 境界値-1（49文字）: 有効
        data_49 = self.valid_supplier_data.copy()
        data_49["supplier_code"] = "A" * 49
        errors = self._validate_serializer(data_49)
        self.assertNotIn("supplier_code", errors)

        # 境界値（50文字）: 有効
        data_50 = self.valid_supplier_data.copy()
        data_50["supplier_code"] = "A" * 50
        errors = self._validate_serializer(data_50)
        self.assertNotIn("supplier_code", errors)

        # 境界値+1（51文字）: 無効
        data_51 = self.valid_supplier_data.copy()
        data_51["supplier_code"] = "A" * 51
        errors = self._validate_serializer(data_51)
        self.assertIn("supplier_code", errors)
        self.assertIn("max_length", str(errors["supplier_code"]))

    # name フィールドのテスト
    def test_name_required(self):
        """
        nameが必須であることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data.pop("name")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("name", errors)
        self.assertIn("この項目は必須です", str(errors["name"]))

    def test_name_empty_string(self):
        """
        nameが空文字の場合エラーになることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
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
        data_199 = self.valid_supplier_data.copy()
        data_199["name"] = "あ" * 199
        errors = self._validate_serializer(data_199)
        self.assertNotIn("name", errors)

        # 境界値（200文字）: 有効
        data_200 = self.valid_supplier_data.copy()
        data_200["name"] = "あ" * 200
        errors = self._validate_serializer(data_200)
        self.assertNotIn("name", errors)

        # 境界値+1（201文字）: 無効
        data_201 = self.valid_supplier_data.copy()
        data_201["name"] = "あ" * 201
        errors = self._validate_serializer(data_201)
        self.assertIn("name", errors)
        self.assertIn("max_length", str(errors["name"]))

    # contact_person フィールドのテスト
    def test_contact_person_boundary_values(self):
        """
        担当者名フィールドの境界値テスト
        境界値-1（99文字）、境界値（100文字）、境界値+1（101文字）の場合をテスト
        """
        # 境界値-1（99文字）: 有効
        data_99 = self.valid_supplier_data.copy()
        data_99["contact_person"] = "あ" * 99
        errors = self._validate_serializer(data_99)
        self.assertNotIn("contact_person", errors)

        # 境界値（100文字）: 有効
        data_100 = self.valid_supplier_data.copy()
        data_100["contact_person"] = "あ" * 100
        errors = self._validate_serializer(data_100)
        self.assertNotIn("contact_person", errors)

        # 境界値+1（101文字）: 無効
        data_101 = self.valid_supplier_data.copy()
        data_101["contact_person"] = "あ" * 101
        errors = self._validate_serializer(data_101)
        self.assertIn("contact_person", errors)
        self.assertIn("max_length", str(errors["contact_person"]))

    # phone フィールドのテスト
    def test_phone_required(self):
        """
        phoneが必須であることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data.pop("phone")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("phone", errors)
        self.assertIn("この項目は必須です", str(errors["phone"]))

    def test_phone_empty_string(self):
        """
        phoneが空文字の場合エラーになることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data["phone"] = ""

        errors = self._validate_serializer(invalid_data)
        self.assertIn("phone", errors)
        self.assertIn("この項目は空にできません", str(errors["phone"]))

    def test_phone_boundary_values(self):
        """
        電話番号フィールドの境界値テスト
        境界値-1（49文字）、境界値（50文字）、境界値+1（51文字）の場合をテスト
        """
        # 境界値-1（49文字）: 有効
        data_49 = self.valid_supplier_data.copy()
        data_49["phone"] = "0" * 49
        errors = self._validate_serializer(data_49)
        self.assertNotIn("phone", errors)

        # 境界値（50文字）: 有効
        data_50 = self.valid_supplier_data.copy()
        data_50["phone"] = "0" * 50
        errors = self._validate_serializer(data_50)
        self.assertNotIn("phone", errors)

        # 境界値+1（51文字）: 無効
        data_51 = self.valid_supplier_data.copy()
        data_51["phone"] = "0" * 51
        errors = self._validate_serializer(data_51)
        self.assertIn("phone", errors)
        self.assertIn("max_length", str(errors["phone"]))

    # email フィールドのテスト
    def test_email_required(self):
        """
        emailが必須であることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data.pop("email")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("email", errors)
        self.assertIn("この項目は必須です", str(errors["email"]))

    def test_email_format(self):
        """
        emailが正しい形式でない場合エラーになることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data["email"] = "invalid-email"  # 無効なメールアドレス

        errors = self._validate_serializer(invalid_data)
        self.assertIn("email", errors)
        self.assertIn("有効なメールアドレスを入力してください", str(errors["email"]))

    def test_email_empty_string(self):
        """
        emailが空文字の場合エラーになることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data["email"] = ""

        errors = self._validate_serializer(invalid_data)
        self.assertIn("email", errors)
        self.assertIn("この項目は空にできません", str(errors["email"]))

    def test_email_boundary_values(self):
        """
        メールアドレスのバリデーションテスト
        """
        # 最小文字数の有効なメール
        min_data = self.valid_supplier_data.copy()
        min_data["email"] = "a@b.co"  # 最小の有効なメールアドレス
        errors = self._validate_serializer(min_data)
        self.assertNotIn("email", errors)

        # 長いメールアドレス（有効）
        long_data = self.valid_supplier_data.copy()
        long_data["email"] = "a" * 50 + "@example.com"
        errors = self._validate_serializer(long_data)
        self.assertNotIn("email", errors)

    # postal_code フィールドのテスト
    def test_postal_code_required(self):
        """
        postal_codeが必須であることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data.pop("postal_code")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("postal_code", errors)
        self.assertIn("この項目は必須です", str(errors["postal_code"]))

    def test_postal_code_empty_string(self):
        """
        postal_codeが空文字の場合エラーになることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data["postal_code"] = ""

        errors = self._validate_serializer(invalid_data)
        self.assertIn("postal_code", errors)
        self.assertIn("この項目は空にできません", str(errors["postal_code"]))

    def test_postal_code_boundary_values(self):
        """
        郵便番号フィールドの境界値テスト
        境界値-1（9文字）、境界値（10文字）、境界値+1（11文字）の場合をテスト
        """
        # 境界値-1（9文字）: 有効
        data_9 = self.valid_supplier_data.copy()
        data_9["postal_code"] = "0" * 9
        errors = self._validate_serializer(data_9)
        self.assertNotIn("postal_code", errors)

        # 境界値（10文字）: 有効
        data_10 = self.valid_supplier_data.copy()
        data_10["postal_code"] = "0" * 10
        errors = self._validate_serializer(data_10)
        self.assertNotIn("postal_code", errors)

        # 境界値+1（11文字）: 無効
        data_11 = self.valid_supplier_data.copy()
        data_11["postal_code"] = "0" * 11
        errors = self._validate_serializer(data_11)
        self.assertIn("postal_code", errors)
        self.assertIn("max_length", str(errors["postal_code"]))

    # prefecture フィールドのテスト
    def test_prefecture_required(self):
        """
        prefectureが必須であることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data.pop("prefecture")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("prefecture", errors)
        self.assertIn("この項目は必須です", str(errors["prefecture"]))

    def test_prefecture_empty_string(self):
        """
        prefectureが空文字の場合エラーになることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data["prefecture"] = ""

        errors = self._validate_serializer(invalid_data)
        self.assertIn("prefecture", errors)
        self.assertIn("この項目は空にできません", str(errors["prefecture"]))

    def test_prefecture_boundary_values(self):
        """
        都道府県フィールドの境界値テスト
        境界値-1（49文字）、境界値（50文字）、境界値+1（51文字）の場合をテスト
        """
        # 境界値-1（49文字）: 有効
        data_49 = self.valid_supplier_data.copy()
        data_49["prefecture"] = "あ" * 49
        errors = self._validate_serializer(data_49)
        self.assertNotIn("prefecture", errors)

        # 境界値（50文字）: 有効
        data_50 = self.valid_supplier_data.copy()
        data_50["prefecture"] = "あ" * 50
        errors = self._validate_serializer(data_50)
        self.assertNotIn("prefecture", errors)

        # 境界値+1（51文字）: 無効
        data_51 = self.valid_supplier_data.copy()
        data_51["prefecture"] = "あ" * 51
        errors = self._validate_serializer(data_51)
        self.assertIn("prefecture", errors)
        self.assertIn("max_length", str(errors["prefecture"]))

    # city フィールドのテスト
    def test_city_required(self):
        """
        cityが必須であることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data.pop("city")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("city", errors)
        self.assertIn("この項目は必須です", str(errors["city"]))

    def test_city_empty_string(self):
        """
        cityが空文字の場合エラーになることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data["city"] = ""

        errors = self._validate_serializer(invalid_data)
        self.assertIn("city", errors)
        self.assertIn("この項目は空にできません", str(errors["city"]))

    def test_city_boundary_values(self):
        """
        市区フィールドの境界値テスト
        境界値-1（99文字）、境界値（100文字）、境界値+1（101文字）の場合をテスト
        """
        # 境界値-1（99文字）: 有効
        data_99 = self.valid_supplier_data.copy()
        data_99["city"] = "あ" * 99
        errors = self._validate_serializer(data_99)
        self.assertNotIn("city", errors)

        # 境界値（100文字）: 有効
        data_100 = self.valid_supplier_data.copy()
        data_100["city"] = "あ" * 100
        errors = self._validate_serializer(data_100)
        self.assertNotIn("city", errors)

        # 境界値+1（101文字）: 無効
        data_101 = self.valid_supplier_data.copy()
        data_101["city"] = "あ" * 101
        errors = self._validate_serializer(data_101)
        self.assertIn("city", errors)
        self.assertIn("max_length", str(errors["city"]))

    # town フィールドのテスト
    def test_town_required(self):
        """
        townが必須であることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data.pop("town")

        errors = self._validate_serializer(invalid_data)
        self.assertIn("town", errors)
        self.assertIn("この項目は必須です", str(errors["town"]))

    def test_town_empty_string(self):
        """
        townが空文字の場合エラーになることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data["town"] = ""

        errors = self._validate_serializer(invalid_data)
        self.assertIn("town", errors)
        self.assertIn("この項目は空にできません", str(errors["town"]))

    def test_town_boundary_values(self):
        """
        町名フィールドの境界値テスト
        境界値-1（199文字）、境界値（200文字）、境界値+1（201文字）の場合をテスト
        """
        # 境界値-1（199文字）: 有効
        data_199 = self.valid_supplier_data.copy()
        data_199["town"] = "あ" * 199
        errors = self._validate_serializer(data_199)
        self.assertNotIn("town", errors)

        # 境界値（200文字）: 有効
        data_200 = self.valid_supplier_data.copy()
        data_200["town"] = "あ" * 200
        errors = self._validate_serializer(data_200)
        self.assertNotIn("town", errors)

        # 境界値+1（201文字）: 無効
        data_201 = self.valid_supplier_data.copy()
        data_201["town"] = "あ" * 201
        errors = self._validate_serializer(data_201)
        self.assertIn("town", errors)
        self.assertIn("max_length", str(errors["town"]))

    # building フィールドのテスト
    def test_building_boundary_values(self):
        """
        建物名フィールドの境界値テスト
        境界値-1（199文字）、境界値（200文字）、境界値+1（201文字）の場合をテスト
        """
        # 境界値-1（199文字）: 有効
        data_199 = self.valid_supplier_data.copy()
        data_199["building"] = "あ" * 199
        errors = self._validate_serializer(data_199)
        self.assertNotIn("building", errors)

        # 境界値（200文字）: 有効
        data_200 = self.valid_supplier_data.copy()
        data_200["building"] = "あ" * 200
        errors = self._validate_serializer(data_200)
        self.assertNotIn("building", errors)

        # 境界値+1（201文字）: 無効
        data_201 = self.valid_supplier_data.copy()
        data_201["building"] = "あ" * 201
        errors = self._validate_serializer(data_201)
        self.assertIn("building", errors)
        self.assertIn("max_length", str(errors["building"]))

    # website フィールドのテスト
    def test_website_special_validation(self):
        """
        websiteフィールドのURLバリデーションをテスト
        """
        # 無効なURL
        invalid_data = self.valid_supplier_data.copy()
        invalid_data["website"] = "invalid-url"

        errors = self._validate_serializer(invalid_data)
        self.assertIn("website", errors)
        self.assertIn("URL", str(errors["website"]))  # URLエラーメッセージを確認

        # 有効なURL
        valid_data = self.valid_supplier_data.copy()
        valid_data["website"] = "https://www.example.com"

        errors = self._validate_serializer(valid_data)
        self.assertNotIn("website", errors)

    # remarks フィールドのテスト
    def test_remarks_empty_string(self):
        """
        remarksが空文字の場合でもエラーにならないことをテスト（必須フィールドではない）
        """
        data = self.valid_supplier_data.copy()
        data["remarks"] = ""

        errors = self._validate_serializer(data)
        self.assertNotIn("remarks", errors)

    # 複数フィールドの組み合わせテスト
    def test_multiple_validation_errors(self):
        """
        複数のフィールドが同時に無効な場合、すべてのエラーが返されることをテスト
        """
        invalid_data = self.valid_supplier_data.copy()
        invalid_data.pop("name")  # 必須フィールドを削除
        invalid_data["email"] = "invalid-email"  # 無効なメールアドレス
        invalid_data["phone"] = ""  # 空の電話番号

        errors = self._validate_serializer(invalid_data)
        self.assertIn("name", errors)
        self.assertIn("email", errors)
        self.assertIn("phone", errors)

    # 正常系のテスト
    def test_valid_data(self):
        """
        有効なデータでエラーが発生しないことをテスト
        """
        errors = self._validate_serializer(self.valid_supplier_data)
        self.assertEqual(len(errors), 0)

    def test_valid_minimal_data(self):
        """
        必須フィールドのみの最小限のデータでエラーが発生しないことをテスト
        """
        minimal_data = {
            "name": "最小限株式会社",
            "phone": "03-9876-5432",
            "email": "info@minimal.co.jp",
            "postal_code": "160-0022",
            "prefecture": "東京都",
            "city": "新宿区",
            "town": "新宿3-1-1",
        }

        errors = self._validate_serializer(minimal_data)
        self.assertEqual(len(errors), 0)

    # supplier_code フィールドの特殊テスト
    def test_supplier_code_empty_string_conversion(self):
        """
        supplier_codeが空文字の場合、Noneに変換されることをテスト
        """
        data = self.valid_supplier_data.copy()
        data["supplier_code"] = ""

        serializer = SupplierSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        # validated_dataでsupplier_codeがNoneになっていることを確認
        self.assertIsNone(serializer.validated_data["supplier_code"])
