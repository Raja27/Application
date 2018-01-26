import logging

from django.contrib.auth import logout, authenticate, login
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from . import serializers

logger = logging.getLogger('django.request')


class Login(APIView):

    def post(self, request, *args, **kwargs):
        response = dict()
        code = status.HTTP_401_UNAUTHORIZED
        data = request.data.copy()
        status_message = "Invalid user credentials"
        try:
            serializer = serializers.LoginSerializer(data=data)
            if serializer.is_valid():
                logger.info('Login data Valid')
                username = serializer.data.get('email').strip().lower()
                password = serializer.data.get('password')
                user_exists = models.User.objects.filter(email=username).exists()
                if not user_exists:
                    status_message = "There is no account associated with this email id"
                    code = status.HTTP_401_UNAUTHORIZED
                else:
                    username = models.User.objects.get(email=username).username
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_superuser:  # for delete
                            login(request, user)
                            response.update({
                                'user_id': user.id,
                                'auth_token': user.get_auth_token()
                            })
                            status_message = 'Successfully logged in.'
                            code = status.HTTP_201_CREATED
                        else:
                            response.update({"user_id": user.id})
                            status_message = "Your account is inactive."
                    else:
                        logger.debug('User: {}'.format(repr(user)))
                        code = status.HTTP_401_UNAUTHORIZED
                        status_message = "Invalid user credentials"
            else:
                code = status.HTTP_206_PARTIAL_CONTENT
                logger.error(repr(serializer.errors))
        except Exception as e:
            logger.error(repr(e))
        response.update({'status_message': status_message})
        return Response(response, code)


class Logout(APIView):
    def post(self, request, *args, **kwargs):
        response = dict()
        code = status.HTTP_401_UNAUTHORIZED
        status_message = "Failed"
        try:
            user = request.user
            logout(request)
            user.delete_auth_token(request.auth)
            code = status.HTTP_201_CREATED
            status_message = "Logged out"
        except Exception as e:
            logger.error(repr(e))
        response.update({'status_message': status_message})
        return Response(response, code)
