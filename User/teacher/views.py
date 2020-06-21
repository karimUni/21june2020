from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 
from User.teacher.serializers import CreateTeacher, RegisterationSerializer
from User.models import User, Teacher, Subject, ActivationKeys
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.contrib.auth import get_user_model
from User.utils import generate_access_token, generate_refresh_token
import jwt
from rest_framework import exceptions
from django.core.mail import send_mail
from django.conf import settings
from User.serializers import CreateStudentWithActivation



@api_view(['POST'])
@permission_classes((AllowAny,))
def registration_teacher(request):
    serializer = RegisterationSerializer(data=request.data)
    serializer2 = CreateTeacher(data=request.data)
    User = get_user_model()
    if serializer.is_valid():
        if serializer2.is_valid():
            user = serializer.save()
            username = user.username
            teacher = serializer2.save(username)
            author = get_object_or_404(User, username=username)
            code = get_object_or_404(ActivationKeys, user=author)
            send_mail('Contact Form', 
                'Ur activation key is {}'.format(code.code),
                settings.EMAIL_HOST_USER,
                ['{}'.format(author.email)],
                fail_silently=False)
        else:
            return Response({'error': serializer2.errors}, 403)
    else:
        return Response({'error': serializer.errors}, 403)

    return Response({'success': 'check your email: {}'.format(author.email)}, 201)


@api_view(['POST'])
@permission_classes([AllowAny])
def active_account(request):
    User = get_user_model()
    code = request.data.get('code')
    response = Response()
    User = get_user_model()
    if (code is None):
        return Response({'error': 'code not found'}, 404)
    
    digits = ActivationKeys.objects.get(code=code)
    if(digits is None):
        return Response({'error': 'invalid code'}, 401)
    user_is = digits.user.username
    active_user = User.objects.filter(username=user_is).first()
    if(active_user is None):
        return Response({'error': 'user not found'}, 404)

    role = RegisterationSerializer(active_user).data['role']
    author = RegisterationSerializer(active_user).data['username']

    access_token = generate_access_token(active_user)
    token_version = Token.objects.get(user=active_user)
    if(token_version is None):
        response.data = {'token_version': 'token version not exist'}
    refresh_token = generate_refresh_token(active_user, token_version)

    response.data = {
        'access_token': access_token,
        'role': role,
        'author': author,
    }

    return response



@api_view(['POST'])
@csrf_exempt
def set_password(request):
    User = get_user_model()
    user = request.user
    editedUser = get_object_or_404(User, username=user.username)
    if (not editedUser):
        return Response({'error': 'user not found'}, 404)
    password = request.data.get('password')
    password2 = request.data.get('password2')
    if password != password2:
        return Response({'error': 'password must match'}, 403)
    editedUser.set_password(password)
    editedUser.save()
    return Response({'success': 'password set'}, 200)
