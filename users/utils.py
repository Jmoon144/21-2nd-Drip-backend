import json, jwt

from django.http import JsonResponse

from drip.production import SECRET_KEY, ALGORITHM

from .models import User

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            user_token    = request.headers.get('Authorization', None)
            decoded_token = jwt.decode(user_token, SECRET_KEY, algorithms=ALGORITHM)
            user          = User.objects.get(id = decoded_token['id'])
            request.user  = user

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            request.user  = None

            return func(self, request, *args, **kwargs)
        
        except jwt.InvalidTokenError:
            return JsonResponse({'message' : 'INVALID_ACCESS_TOKEN'})
    
    return wrapper