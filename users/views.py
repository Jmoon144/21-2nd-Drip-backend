import jwt, requests

from django.views     import View
from django.http      import JsonResponse
from django.db.utils import IntegrityError

from .models        import User
from drip.env  import SECRET_KEY, ALGORITHM

class KakaoSigninView(View):
    def post(self, request):
        try:
            access_token = request.headers.get("Authorization")
            
            if not access_token:
                return JsonResponse({'message' : 'ACCESS_TOKEN_DOES_NOT_EXITS'}, status=401)

            headers   = ({'Authorization':f'Bearer {access_token}'})
            kakao_url = 'https://kapi.kakao.com/v2/user/me'
            response  = requests.get(kakao_url, headers = headers)
            user      = response.json()
            
            if not user:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)

            user, created = User.objects.get_or_create(
                name          = user['kakao_account']['profile'].get('nickname'),
                email         = user['kakao_account'].get('email'),
                profile_image = user['kakao_account']['profile'].get('profile_image_url'),
                origin_pk     = user.get('id')
            )
            
            result = {
                'name'          : user.name,
                'profile_image' : user.profile_image,
                'email'         : user.email
            }
            token = jwt.encode({'id' : user.id}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'token' : token, 'data' : result}, status = 201)
            
        except IntegrityError:
            return JsonResponse({'message' : 'INTEGRITY_ERROR'}, status=401)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
