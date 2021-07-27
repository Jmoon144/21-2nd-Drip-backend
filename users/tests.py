import unittest, jwt

from django.test import Client, TestCase
from unittest.mock import patch, MagicMock

from drip.env import SECRET_KEY, ALGORITHM
from .models import User

class SigninTest(TestCase):
    @patch('users.views.requests')
    def test_signin_succes(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'kakao_account' : {
                        'email' : 'sjwm98@mail.com',
                        'profile' : {
                            'profile_image_url' : 'akldaskda',
                            'nickname' : '박준영123'
                        }
                    },
                    'id' : '1'    
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': 'fake_token'}
        response            = client.post('/users/signin', content_type='applications/json', **headers)
        user                = User.objects.get(email = 'sjwm98@mail.com')

        result = {
            'name' : user.name,
            'email' : user.email,
            'profile_image' : user.profile_image
        }
        
        token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHM)
        
        self.assertEqual(response.json(), {'token' : token, 'data' : result})
        self.assertEqual(response.status_code, 201)
        
    @patch('users.views.requests')
    def test_signin_access_token_does_not_exit(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'kakao_account' : {
                        'email' : 'sjwm98@mail.com',
                        'profile' : {
                            'profile_image_url' : 'akldaskda',
                            'nickname' : '박준영'
                        }
                    },
                    'id' : '1'    
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': ''}
        response            = client.post('/users/signin', content_type='applications/json', **headers)

        self.assertEqual(response.json(), {'message' : 'ACCESS_TOKEN_DOES_NOT_EXITS'})
        self.assertEqual(response.status_code, 401)

    @patch('users.views.requests')
    def test_signin_key_error(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'kakao_accocunt' : {
                        'email' : 'sjwm98@mail.com',
                        'profile' : {
                            'profile_image_url' : 'akldaskda',
                            'nickname' : '박준영'
                        }
                    },
                    'id' : '1'    
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': 'fake_token'}
        response            = client.post('/users/signin', content_type='applications/json', **headers)
        
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})
        self.assertEqual(response.status_code, 400)
    
    @patch('users.views.requests')
    def test_signin_invalid_token(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                       
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': 'fake_token'}
        response            = client.post('/users/signin', content_type='applications/json', **headers)

        self.assertEqual(response.json(), {'message' : 'INVALID_TOKEN'})
        self.assertEqual(response.status_code, 401)

    @patch('users.views.requests')
    def test_signin_integrity_error(self, mocked_requests):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'kakao_account' : {
                        'email' : 'sjwm98@mail.com',
                        'profile' : {
                            'profile_image_url' : 'akldaskda',
                            'nickname' : '박준영'
                        }
                    },    
                }

        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'HTTP_Authorization': 'fake_token'}
        response            = client.post('/users/signin', content_type='applications/json', **headers)
        
        self.assertEqual(response.json(), {'message' : 'INTEGRITY_ERROR'})
        self.assertEqual(response.status_code, 401)