import jwt, json

from django.test     import TestCase, Client

from orders.models   import Order, Status
from products.models import Category, Product, Search, SubCategory
from users.models    import User
from drip.production   import SECRET_KEY, ALGORITHM
from reviews.models  import Review

class OrderViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.bulk_create([
            User(id=1, name='aaa', email='a0@b.c', profile_image='abc', origin_pk=1),
            User(id=2, name='aaa', email='a1@b.c', profile_image='abc', origin_pk=2),
            User(id=3, name='aaa', email='a2@b.c', profile_image='abc', origin_pk=3),
        ])
        Search.objects.create(id=1, count=5)
        Category.objects.create(id=1, name='아웃도어')
        SubCategory.objects.create(id=1, name='액티비티', discount=0.1, category_id=1)
        Product.objects.bulk_create([
            Product(
                id              = 1,
                name            = 'aaa',
                price           = 48000,
                main_image      = 'aaa',
                description     = 'aaa',
                address         = '서울 서초구 방배천로 11',
                sell_count      = 1230,
                date            = '2021-6-5',
                latitude        = None,
                longitude       = None,
                sub_category_id = 1,
                searched_id     = 1)
        ])
        Status.objects.bulk_create([
            Status(id=1, name='북마크'),
            Status(id=2, name='구매완료'),
            Status(id=3, name='사용기간만료')
        ])
        Order.objects.bulk_create([
            Order(id=1, product_id=1, status_id=1, user_id=1),
            Order(id=2, product_id=1, status_id=2, user_id=1),
            Order(id=3, product_id=1, status_id=3, user_id=1),
        ])
        Review.objects.create(
            content   = 'aaa',
            image_url = 'aaa',
            rating    = 4.5,
            product   = Product.objects.get(id=1),
            user      = User.objects.get(id=1)
        )

        cls.token = jwt.encode({'id' : User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)
    
    def test_post_success(self):
        client  = Client()
        headers = {'HTTP_Authorization' : self.token}
        payload = {
            'product_id' : 1
        }

        response = client.post('/orders', payload, **headers, content_type='application/json')
        
        self.assertEqual(response.json(), {'message' : 'SUCCESS'})
        self.assertEqual(response.status_code, 201)
    
    def test_if_wrong_key(self):
        client  = Client()
        headers = {'HTTP_Authorization' : self.token}
        payload = {
            'idid' : 1
        }

        response = client.post('/orders', payload, **headers, content_type='application/json')

        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
        self.assertEqual(response.status_code, 400)

    def test_if_wrong_product_id(self):
        client  = Client()
        headers = {'HTTP_Authorization' : self.token}
        payload = {
            'product_id' : 60
        }

        response = client.post('/orders', payload, **headers, content_type='application/json')

        self.assertEqual(response.json(), {'message' : 'PRODUCT_NOT_EXIST'})
        self.assertEqual(response.status_code, 400)

    def test_if_empty_body(self):
        client  = Client()
        headers = {'HTTP_Authorization' : self.token}

        response = client.post('/orders', **headers)

        self.assertEqual(response.json(), {'message' : 'EMPTY_BODY_DATA'})
        self.assertEqual(response.status_code, 400)

    def test_get_success(self):
        client  = Client()
        headers = {'HTTP_Authorization' : self.token}

        response = client.get('/orders?status=2&offset=0&limit=1', **headers)

        result = {
            'result' : {
                'user_info': {
                    'name': 'aaa', 
                    'profile_image': 'abc'
                    }, 
                'result': [{
                    'product_id': 1, 
                    'name': 'aaa', 
                    'price': '48000.0', 
                    'image': 'aaa', 
                    'new': True, 
                    'hot': True, 
                    'discount': '0.10', 
                    'rating': '4.50000'
                    }], 
                'pages' : 1
                }
            }

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

class BookMarkTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.bulk_create([
            User(id=1, name='aaa', email='a0@b.c', profile_image='abc', origin_pk=1),
            User(id=2, name='aaa', email='a1@b.c', profile_image='abc', origin_pk=2),
            User(id=3, name='aaa', email='a2@b.c', profile_image='abc', origin_pk=3),
        ])
        Search.objects.create(id=1, count=5)
        Category.objects.create(id=1, name='아웃도어')
        SubCategory.objects.create(id=1, name='액티비티', discount=0.1, category_id=1)
        Product.objects.bulk_create([
            Product(
                id              = 1,
                name            = 'aaa',
                price           = 48000,
                main_image      = 'aaa',
                description     = 'aaa',
                address         = '서울 서초구 방배천로 11',
                sell_count      = 1230,
                date            = '2021-6-5',
                latitude        = None,
                longitude       = None,
                sub_category_id = 1,
                searched_id     = 1)
        ])
        Status.objects.bulk_create([
            Status(id=1, name='북마크'),
            Status(id=2, name='구매완료'),
            Status(id=3, name='사용기간만료')
        ])
        Order.objects.bulk_create([
            Order(id=1, product_id=1, status_id=1, user_id=1),
            Order(id=2, product_id=1, status_id=2, user_id=1),
            Order(id=3, product_id=1, status_id=3, user_id=1),
        ])
        Review.objects.create(
            content   = 'aaa',
            image_url = 'aaa',
            rating    = 4.5,
            product   = Product.objects.get(id=1),
            user      = User.objects.get(id=1)
        )

        cls.token = jwt.encode({'id' : User.objects.get(id=1).id}, SECRET_KEY, ALGORITHM)

    # def test_post_success(self):
    #     client  = Client()
        
    #     headers = {'HTTP_Authorization' : self.token}
    #     payload = {'product_id' : 1}
        
    #     response = client.post('/orders/bookmark', payload, content_type='application/json', **headers)
    #     self.assertEqual.__self__.maxDiff = None
    #     maxDiff = None
    #     self.assertEqual(response.status_code, 204)
    #     self.assertEqual(response.json(), {'message' : 'SUCCESS'})

    # def test_post_success2(self):
    #     client  = Client()
    #     headers = {'HTTP_Authorization' : self.token}
    #     payload = {
    #         'product_id' : '1'
    #     }
        
    #     response = client.post('/orders/bookmark', json.dumps(payload), **headers, content_type='application/json')
    #     self.assertEqual(response.json(), {'message' : 'SUCCESS'})
    #     self.assertEqual(response.status_code, 201)

    # def test_post_sus(self):
    #     client  = Client()
    #     headers = {'HTTP_Authorization' : self.token}
    #     payload = {
    #         'product_id' : 1
    #     }
    #     print(payload)

    #     response = client.post('/orders/bookmark', payload, **headers, content_type='application/json')
    #     print(response.json())

    #     # self.assertEqual(response.json(), {'message' : 'PRODUCT_NOT_EXIST'})
    #     self.assertEqual(response.status_code, 400)