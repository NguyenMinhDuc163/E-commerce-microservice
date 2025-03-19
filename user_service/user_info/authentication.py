# xác thưc tùy chỉnh
import jwt
from django.conf import settings
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from user_model.models import Account


class SafeJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print(request.headers)
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None

        try:
            token_prefix, access_token = authorization_header.split(' ')
            if token_prefix != 'Bearer':
                raise exceptions.AuthenticationFailed('Invalid token prefix')

            payload = jwt.decode(access_token,
                                 settings.SECRET_KEY,
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Access token expired')
        except ValueError:
            raise exceptions.AuthenticationFailed('Invalid token format')
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed('Invalid token')

        username = payload.get('username')
        if username is None:
            raise exceptions.AuthenticationFailed('User ID not found in token payload')

        user = Account.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        # if not user.is_active:
        #     raise exceptions.AuthenticationFailed('User is not active')

        return (user, None)