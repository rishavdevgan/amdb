# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from users.models import User
from users.models import AccessToken
from users.serializers import UserSerializer
from django.contrib.auth import logout
from django.http import HttpResponse


# Create your views here.


@api_view(['POST'])
def create_user(request):

    name = request.data['name']
    username = request.data['username']
    password = request.data['password']
    short_bio = request.data['short_bio']

    if name is None or len(name) == 0:
        return Response({"error message": "Name field cannot be empty!!"}, status=400)

    if password is None or len(password) < 6:
        return Response({"error message": "Password has to be atleast 6 characters long!!"}, status=400)

    does_username_exists = User.objects.filter(username=username).first()

    if does_username_exists is not None:
        return Response({"error_message":"Username already  exists! Please choose a unique username"}, status=400)

    new_user = User(name=name, username=username, password=make_password(password), short_bio=short_bio)

    new_user.save()

    return Response(UserSerializer(instance=new_user).data, status=200)


@api_view(['GET'])
def get_user(request):
    print request.query_params

    if 'user_id' in request.query_params:
        user = User.objects.filter(id=request.query_params['user_id'])
        if len(user) > 0:
            return Response(UserSerializer(instance=user[0]).data, status=200)
        else:
            return Response({"message": "User not found! Sorry."}, status=200)
    else:

        users = User.objects.all()

        return Response(UserSerializer(instance=users, many=True).data, status=200)


@api_view(['POST'])
def login_user(request):

    username = None
    password = None

    if 'username' in request.data:
        username = request.data['username']

    if 'password' in request.data:
        password = request.data['password']

    if not username or not password:
        return Response({"message": "Username or Password not provided. Invalid request"}, status=200)

    user = User.objects.filter(username=username).first()

    if user:

        if not check_password(password, user.password):
            return Response({"message": "Username or password in invalid."}, status=200)
        else:
            token = AccessToken(user=user)
            token.create_token()
            token.save()
            return Response({"token": token.access_token}, status=200)

    else:
        return Response({"message": "Username or password is invalid."}, status=200)


def check_token():
    access_token = request.META['HTTP_TOKEN']

    token_exists = AccessToken.objects.filter(access_token=access_token, is_valid=True).first()

    if not token_exists:
        return None
    else:
        return token_exists.user


@api_view(['POST'])
def create_movie(request):

    current_user = check_token(request)

    if current_user:
        print current_user.username
    else:
        return Response({"message": "You are not authorized to perform this action"}, status=400)


@api_view(['POST'])
def review_movie(request):

    current_user = check_token(request)

    if current_user:
        print current_user.username
    else:
        return Response({"message": "You are not authorized to perform this action"}, status=400)


@api_view(['GET'])
def logout(request):

    check_token(request)

    if 'access_token' in request.META['HTTP_TOKEN']:

        return Response({"message": "Success."}, status=200)

        logout(request)

    else:

        return Response({"message": "User not found."}, status=400)








