from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from django.utils.translation import gettext_lazy as _

import jwt
from datetime import datetime,timedelta,timezone

from .menager import UserMenager
import credensial


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth or auth.split(" ")[0]!="Bearer":
            return None
        auth_token = auth.split(" ")[1]

        menager = JWTMenager()
        payload = menager.decode(auth_token)
        
        if not payload:
            raise exceptions.AuthenticationFailed(_('JWT Token expired.'))
        if payload["token_type"]!="access":
            raise exceptions.AuthenticationFailed(_('JWT Token must be access type.'))

        user = UserMenager.get_user(payload["user_id"])

        return (user,None)


class JWTToken():
    def __init__(self):
        self._private_key = credensial.private_key
        self._public_key = credensial.public_key

    def create_access_token(self,user):
        payload = {
            "user_id":user.id,
            "token_type":"access",
            "exp":datetime.now(tz=timezone.utc)+timedelta(minutes=15)
        }
        return jwt.encode(payload,self._private_key,"RS512")

    def create_refresh_token(self,user):
        payload = {
            "user_id":user.id,
            "token_type":"refresh",
            "exp":datetime.now(tz=timezone.utc)+timedelta(days=1)
        }
        return jwt.encode(payload,self._private_key,"RS512")

    def decode_token(self,token):
        return jwt.decode(token,self._public_key,"RS512")

class JWTMenager():
    def __init__(self):
        self._token = JWTToken()

    def login(self,user):
        return {
            "access":self._token.create_access_token(user),
            "refresh":self._token.create_refresh_token(user)
        }

    def decode(self,token):
        try:
            decode = self._token.decode_token(token)
            return decode
        except jwt.ExpiredSignatureError:
            return None

    def create_new_token(self,token):
        payload = self._token.decode_token(token)
        if not payload:
            raise exceptions.ParseError(_("JWT Token expired"))
        if payload["token_type"]!="refresh":
            raise exceptions.ParseError(_("JWT Token must be refresh type"))

        user = UserMenager.get_user(payload["user_id"])
        return {"access":self._token.create_access_token(user)}
