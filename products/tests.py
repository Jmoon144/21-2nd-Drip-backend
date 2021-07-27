import json, jwt

from django.test import TestCase, Client

from unittest.mock import patch

from .models        import Category, Search, SubCategory, Product
from reviews.models import Review
from users.models   import User
from orders.models  import Order, Status
from drip.production  import SECRET_KEY, ALGORITHM

class ProductListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(id=1, name="test")
        SubCategory.objects.create(id=1, name="test1",category_id=1,discount=0.20)
        SubCategory.objects.create(id=2, name="test2",category_id=1,discount=0.30)
        SubCategory.objects.create(id=3, name="test3",category_id=1,discount=0.50)
        Search.objects.create(id=1, count=0)
        User.objects.create(
            id            = 1,
            email         = "test1@test.kr",
            name          = "최승리",
            profile_image = "test.url"
        )
        User.objects.create(
            id            = 2,
            email         = "test2@test.kr",
            name          = "김승리",
            profile_image = "test.url"
        )
        User.objects.create(
            id            = 3,
            email         = "tes3@test.kr",
            name          = "박승리",
            profile_image = "test.url"
        )
        User.objects.create(
            id            = 4,
            email         = "tes4@test.kr",
            name          = "정승리",
            profile_image = "test.url"
        )
        Product.objects.create(
            id              = 1,
            name            = "서핑",
            price           = 20000,
            main_image      = "test_url",
            description     = "test_des_url",
            sub_category_id = 1,
            address         = "서울특별시 강남구 강남대로 123-4",
            sell_count      = 11,
            searched_id     = 1,
            date            = "2021-06-10"
        )
        Product.objects.create(
            id              = 2,
            name            = "보드",
            price           = 30000,
            main_image      = "test_url",
            description     = "test_des_url",
            sub_category_id = 2,
            address         = "세종특별시 강남구 선릉대로 123-4",
            sell_count      = 10,
            searched_id     = 1,
            date            = "2021-06-03"
        )
        Product.objects.create(
            id              = 3,
            name            = "수영",
            price           = 40000,
            main_image      = "test_url",
            description     = "test_des_url",
            sub_category_id = 3,
            address         = "인천광역시 강남구 선릉대로 123-4",
            sell_count      = 15,
            searched_id     = 1,
            date            = "2021-06-21"
        )
        Product.objects.create(
            id              = 4,
            name            = "유도",
            price           = 50000,
            main_image      = "test_url",
            description     = "test_des_url",
            sub_category_id = 1,
            address         = "목포시 하당동 하당로로 123-4",
            sell_count      = 1119,
            searched_id     = 1,
            date            = "2021-06-01"
        )
        Review.objects.create(
            id         = 1,
            content    = "굿굿굿굿",
            image_url  = "test_url",
            rating     = 5.0,
            product_id = 1,
            user_id    = 1
        )
        Review.objects.create(
            id         = 2,
            content    = "좋아좋아",
            image_url  = "test_url",
            rating     = 4.0,
            product_id = 2,
            user_id    = 2
        )
        Review.objects.create(
            id         = 3,
            content    = "싫어싫어",
            image_url  = "test_url",
            rating     = 2.0,
            product_id = 3,
            user_id    = 3
        )
        Review.objects.create(
            id         = 4,
            content    = "그냥그래",
            image_url  = "test_url",
            rating     = 3.0,
            product_id = 4,
            user_id    = 4
        )
        Status.objects.create(
            id   = 1,
            name = "북마크"
        )
        Status.objects.create(
            id   = 2,
            name = "사용전"
        )
        Status.objects.create(
            id   = 3,
            name = "사용완료"
        )
        Order.objects.create(
            user_id    = 1,
            status_id  = 1,
            product_id = 1
        )

        cls.token = jwt.encode({"id":User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        User.objects.all().delete()
        Product.objects.all().delete()
        Review.objects.all().delete()
        Search.objects.all().delete()

    def test_list_get_new_view(self):
        client = Client()
        self.assertEqual.__self__.maxDiff = None
        headers = {'HTTP_Authorization': self.token}
        print(self.token)
        response = client.get('/products?sortMethod=date&reverse=True&limit=4', content_type='application/json', **headers)
        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "product_id": 3,
                        "product_name": "수영",
                        "address": "인천광역시",
                        "product_price": "40000.0",
                        "discount": "20000.000",
                        "product_image": "test_url",
                        "sellcount": 15,
                        "avg_score": "2.00",
                        "date": "2021-06-21",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                    {
                        "product_id": 1,
                        "product_name": "서핑",
                        "address": "서울특별시",
                        "product_price": "20000.0",
                        "discount": "16000.000",
                        "product_image": "test_url",
                        "sellcount": 11,
                        "avg_score": "5.00",
                        "date": "2021-06-10",
                        "new": True,
                        "hot": True,
                        "check": True
                    },
                    {
                        "product_id": 2,
                        "product_name": "보드",
                        "address": "세종특별시",
                        "product_price": "30000.0",
                        "discount": "21000.000",
                        "product_image": "test_url",
                        "sellcount": 10,
                        "avg_score": "4.00",
                        "date": "2021-06-03",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                    {
                        "product_id": 4,
                        "product_name": "유도",
                        "address": "목포시",
                        "product_price": "50000.0",
                        "discount": "40000.000",
                        "product_image": "test_url",
                        "sellcount": 1119,
                        "avg_score": "3.00",
                        "date": "2021-06-01",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_list_get_best_view(self):
        client = Client()
        self.assertEqual.__self__.maxDiff = None
        headers = {'HTTP_Authorization': self.token}
        response = client.get('/products?sortMethod=sellcount&reverse=True&limit=4', **headers)
        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "product_id": 4,
                        "product_name": "유도",
                        "address": "목포시",
                        "product_price": "50000.0",
                        "discount": "40000.000",
                        "product_image": "test_url",
                        "sellcount": 1119,
                        "avg_score": "3.00",
                        "date": "2021-06-01",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                    {
                        "product_id": 3,
                        "product_name": "수영",
                        "address": "인천광역시",
                        "product_price": "40000.0",
                        "discount": "20000.000",
                        "product_image": "test_url",
                        "sellcount": 15,
                        "avg_score": "2.00",
                        "date": "2021-06-21",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                    {
                        "product_id": 1,
                        "product_name": "서핑",
                        "address": "서울특별시",
                        "product_price": "20000.0",
                        "discount": "16000.000",
                        "product_image": "test_url",
                        "sellcount": 11,
                        "avg_score": "5.00",
                        "date": "2021-06-10",
                        "new": True,
                        "hot": True,
                        "check": True
                    },
                    {
                        "product_id": 2,
                        "product_name": "보드",
                        "address": "세종특별시",
                        "product_price": "30000.0",
                        "discount": "21000.000",
                        "product_image": "test_url",
                        "sellcount": 10,
                        "avg_score": "4.00",
                        "date": "2021-06-03",
                        "new": True,
                        "hot": True,
                        "check": False
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_list_get_category_view(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}
        self.assertEqual.__self__.maxDiff = None
        response = client.get('/products?categoryId=1', **headers)
        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "product_id": 1,
                        "product_name": "서핑",
                        "address": "서울특별시",
                        "product_price": "20000.0",
                        "discount": "16000.000",
                        "product_image": "test_url",
                        "sellcount": 11,
                        "avg_score": "5.00",
                        "date": "2021-06-10",
                        "new": True,
                        "hot": True,
                        "check": True
                    },
                    {
                        "product_id": 2,
                        "product_name": "보드",
                        "address": "세종특별시",
                        "product_price": "30000.0",
                        "discount": "21000.000",
                        "product_image": "test_url",
                        "sellcount": 10,
                        "avg_score": "4.00",
                        "date": "2021-06-03",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                    {
                        "product_id": 3,
                        "product_name": "수영",
                        "address": "인천광역시",
                        "product_price": "40000.0",
                        "discount": "20000.000",
                        "product_image": "test_url",
                        "sellcount": 15,
                        "avg_score": "2.00",
                        "date": "2021-06-21",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                    {
                        "product_id": 4,
                        "product_name": "유도",
                        "address": "목포시",
                        "product_price": "50000.0",
                        "discount": "40000.000",
                        "product_image": "test_url",
                        "sellcount": 1119,
                        "avg_score": "3.00",
                        "date": "2021-06-01",
                        "new": True,
                        "hot": True,
                        "check": False
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_list_get_subcategory_view(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}
        self.assertEqual.__self__.maxDiff = None
        response = client.get('/products?subcategoryId=1', **headers)
        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "product_id": 1,
                        "product_name": "서핑",
                        "address": "서울특별시",
                        "product_price": "20000.0",
                        "discount": "16000.000",
                        "product_image": "test_url",
                        "sellcount": 11,
                        "avg_score": "5.00",
                        "date": "2021-06-10",
                        "new": True,
                        "hot": True,
                        "check": True
                    },
                    {
                        "product_id": 4,
                        "product_name": "유도",
                        "address": "목포시",
                        "product_price": "50000.0",
                        "discount": "40000.000",
                        "product_image": "test_url",
                        "sellcount": 1119,
                        "avg_score": "3.00",
                        "date": "2021-06-01",
                        "new": True,
                        "hot": True,
                        "check": False
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_list_get_subcategory_sort1_view(self):
        client = Client()
        headers = {'HTTP_Authorization': self.token}
        self.assertEqual.__self__.maxDiff = None
        response = client.get('/products?subcategoryId=1&sortMethod=discount&reverse=True', **headers)
        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "product_id": 4,
                        "product_name": "유도",
                        "address": "목포시",
                        "product_price": "50000.0",
                        "discount": "40000.000",
                        "product_image": "test_url",
                        "sellcount": 1119,
                        "avg_score": "3.00",
                        "date": "2021-06-01",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                    {
                        "product_id": 1,
                        "product_name": "서핑",
                        "address": "서울특별시",
                        "product_price": "20000.0",
                        "discount": "16000.000",
                        "product_image": "test_url",
                        "sellcount": 11,
                        "avg_score": "5.00",
                        "date": "2021-06-10",
                        "new": True,
                        "hot": True,
                        "check": True
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_list_get_subcategory_sort2_view(self):
        client = Client()
        self.assertEqual.__self__.maxDiff = None
        headers = {'HTTP_Authorization': self.token}
        response = client.get('/products?subcategoryId=1&sortMethod=discount', **headers)
        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "product_id": 1,
                        "product_name": "서핑",
                        "address": "서울특별시",
                        "product_price": "20000.0",
                        "discount": "16000.000",
                        "product_image": "test_url",
                        "sellcount": 11,
                        "avg_score": "5.00",
                        "date": "2021-06-10",
                        "new": True,
                        "hot": True,
                        "check": True
                    },
                    {
                        "product_id": 4,
                        "product_name": "유도",
                        "address": "목포시",
                        "product_price": "50000.0",
                        "discount": "40000.000",
                        "product_image": "test_url",
                        "sellcount": 1119,
                        "avg_score": "3.00",
                        "date": "2021-06-01",
                        "new": True,
                        "hot": True,
                        "check": False
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_list_get_subcategory_sort3_view(self):
        client = Client()
        self.assertEqual.__self__.maxDiff = None
        headers = {'HTTP_Authorization': self.token}
        response = client.get('/products?subcategoryId=1&sortMethod=sellcount&reverse=True', **headers)
        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "product_id": 4,
                        "product_name": "유도",
                        "address": "목포시",
                        "product_price": "50000.0",
                        "discount": "40000.000",
                        "product_image": "test_url",
                        "sellcount": 1119,
                        "avg_score": "3.00",
                        "date": "2021-06-01",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                    {
                        "product_id": 1,
                        "product_name": "서핑",
                        "address": "서울특별시",
                        "product_price": "20000.0",
                        "discount": "16000.000",
                        "product_image": "test_url",
                        "sellcount": 11,
                        "avg_score": "5.00",
                        "date": "2021-06-10",
                        "new": True,
                        "hot": True,
                        "check": True
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_list_get_subcategory_sort4_view(self):
        client = Client()
        self.assertEqual.__self__.maxDiff = None
        headers = {'HTTP_Authorization': self.token}
        response = client.get('/products?subcategoryId=1&sortMethod=avg_score&reverse=True', **headers)
        self.assertEqual(response.json(),
            {
                "result": [
                    {
                        "product_id": 1,
                        "product_name": "서핑",
                        "address": "서울특별시",
                        "product_price": "20000.0",
                        "discount": "16000.000",
                        "product_image": "test_url",
                        "sellcount": 11,
                        "avg_score": "5.00",
                        "date": "2021-06-10",
                        "new": True,
                        "hot": True,
                        "check": True
                    },
                    {
                        "product_id": 4,
                        "product_name": "유도",
                        "address": "목포시",
                        "product_price": "50000.0",
                        "discount": "40000.000",
                        "product_image": "test_url",
                        "sellcount": 1119,
                        "avg_score": "3.00",
                        "date": "2021-06-01",
                        "new": True,
                        "hot": True,
                        "check": False
                    },
                ]
            }
        )
        self.assertEqual(response.status_code, 200)