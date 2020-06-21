from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from User.models import DigitsSecurity
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import random
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 
from User.utils import generate_access_token, generate_refresh_token
from rest_framework.authtoken.models import Token
from User.serializers import RegisterationSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
# @ensure_csrf_cookie
@csrf_exempt
def send_email(request):
    User = get_user_model()
    email = request.data.get('email')

    try:
        user = get_object_or_404(User, email=email)
        # user = get_object_or_404(User, username='shimaa')
    except:
        return Response({'error': 'user not found'}, 404)

    new_user = int(user.id)
    digits = [0, 0, 0, 0, 0, 0]
    Secret_digits = ""
    for i in digits:
        Secret_digit = int(random.random() * 10)
        Secret_digits += str(Secret_digit)
    new_Secret_digits = DigitsSecurity(id=None, user=user, digits=Secret_digits)
    new_Secret_digits.save()
    send_mail('Contact Form', 
    'Ur secret key is {}'.format(Secret_digits),
    settings.EMAIL_HOST_USER,
    ['{}'.format(email)],
    fail_silently=False)

    return HttpResponse('success')



@api_view(['POST'])
@permission_classes([AllowAny])
# @ensure_csrf_cookie
@csrf_exempt
def recieve_email(request):
    User = get_user_model()
    code = request.data.get('code')
    response = Response()
    if (code is None):
        return Response({'error': 'code not found'}, 404)
    
    digits = DigitsSecurity.objects.get(digits=code)
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
def reset_password(request):
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
    return Response({'success': 'password reset'}, 200)
