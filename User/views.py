# Notes this views.py only for registraion
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 
from User.serializers import RegisterationSerializer, CreateHeadMaster, CreateTeacher, CreateStudent, CreateParent, CreateStudentWithActivation, UpdateStudentWithActivation
from .models import User, HeadMaster, Teacher, Subject, ActivationKeys, Student
from rest_framework.authtoken.models import Token

from django.contrib.auth import get_user_model
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from User.utils import generate_access_token, generate_refresh_token
import jwt
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from rest_framework import exceptions
from User.teacher.serializers import RegisterationSerializer as _user
from User.decorators import teacher_role
from django.core.mail import send_mail


#head master registeration view
@api_view(['POST'])
@permission_classes((AllowAny,))
def registration_headmaster_view(request):
    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        serializer2 = CreateHeadMaster(data=request.data)
        data = {}
        if serializer.is_valid() and serializer2.is_valid():
            user = serializer.save()
            data['respone'] = 'Successful registrated a new user'
            data['email'] = user.email
            data['username'] = user.username
            data['role'] = user.role
            data['address'] = user.address
            data['phone'] = user.phone_number
            data['birth_date'] = user.birth_date
            token = Token.objects.get(user=user).key
            data['token'] = token
            headmaster = serializer2.save(user=user)
            data['uni_code'] = headmaster.uni_code
            data['educationalType'] = headmaster.educational_type
        else:
            data = serializer.errors
            data += serializer2.errors
        return Response(data)


#teacher registeration view
@api_view(['POST'])
@permission_classes((AllowAny,))
def registration_teacher_view(request):
    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        serializer2 = CreateTeacher(data=request.data)
        data = {}
        if serializer.is_valid():
            if serializer2.is_valid():
                user = serializer.save()
                data['respone'] = 'Successful registrated a new user'
                data['email'] = user.email
                data['username'] = user.username
                data['role'] = user.role
                data['address'] = user.address
                data['phone'] = user.phone_number
                data['birth_date'] = user.birth_date
                token = Token.objects.get(user=user).key
                data['token'] = token
                username = user.username
                teacher = serializer2.save(username)
                data['uni_code'] = teacher.uni_code
                data['grade'] = teacher.grade
                data['level'] = teacher.level
            else:
                data = serializer2.errors
        else:
            data = serializer.errors
        return Response(data)


#student registeration view
@api_view(['POST'])
@permission_classes((AllowAny,))
def registration_student_view(request):
    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        serializer2 = CreateStudent(data=request.data)
        data = {}
        if serializer.is_valid():
            if serializer2.is_valid():
                user = serializer.save()
                data['respone'] = 'Successful registrated a new user'
                data['email'] = user.email
                data['username'] = user.username
                data['role'] = user.role
                data['address'] = user.address
                data['phone'] = user.phone_number
                data['birth_date'] = user.birth_date
                token = Token.objects.get(user=user).key
                data['token'] = token
                username = user.username
                student = serializer2.save(username)
                data['uni_code'] = student.uni_code
                data['grade'] = student.grade
                data['level'] = student.level
            else:
                data = serializer2.errors
        else:
            data = serializer.errors
        return Response(data)


#parent registeration view
@api_view(['POST'])
@permission_classes((AllowAny,))
def registration_parent_view(request):
    if request.method == 'POST':
        serializer = RegisterationSerializer(data=request.data)
        serializer2 = CreateParent(data=request.data)
        data = {}
        if serializer.is_valid():
            if serializer2.is_valid():
                user = serializer.save()
                data['respone'] = 'Successful registrated a new user'
                data['email'] = user.email
                data['username'] = user.username
                data['role'] = user.role
                data['address'] = user.address
                data['phone'] = user.phone_number
                data['birth_date'] = user.birth_date
                token = Token.objects.get(user=user).key
                data['token'] = token
                username = user.username
                parent = serializer2.save(username)
                data['uni_code'] = parent.uni_code
            else:
                data = serializer2.errors
        else:
            data = serializer.errors
        return Response(data)



@api_view(['POST'])
@permission_classes([AllowAny])
#@ensure_csrf_cookie
@csrf_exempt
def login_view(request):
    User = get_user_model()
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = User.objects.filter(username=username).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')

    role = RegisterationSerializer(user).data['role']
    author = RegisterationSerializer(user).data['username']

    access_token = generate_access_token(user)
    token_version = Token.objects.get(user=user)
    if(token_version is None):
        response.data = {'token_version': 'token version not exist'}
    refresh_token = generate_refresh_token(user, token_version)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    try:
        headers = request.headers.items()
        tokens = ''
        for header in headers:
            if 'Cookie' in header:
                tokens = header[1]
                break
    except:
        tokens = 'error'
    response.data = {
        'access_token': access_token,
        'role': role,
        'author': author,
        'tokens': tokens
    }

    return response

# def login_form_view(request):


# llll
@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def refresh_token_view(request):
    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''
    User = get_user_model()
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            'Authentication credentials were not provided.')
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if (user is None):
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')

    user_token_version = Token.objects.filter(user=user).first()
    if user_token_version.token_version != payload.get('token_version'):
        raise exceptions.AuthenticationFailed(
            'revoked refresh token, user not authenticated.')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})



@ensure_csrf_cookie
def set_csrf_token(request):

    try:
        headers = request.headers.items()
    except:
        headers = "None"
    return JsonResponse({"details": "CSRF cookie set", "Headers": headers})



@api_view(['POST', 'GET'])
@teacher_role
def registration_student(request):
    user = request.user
    if request.method == 'POST':
        serializer = _user(data=request.data)
        serializer2 = CreateStudentWithActivation(data=request.data)
        User = get_user_model()
        if serializer.is_valid():
            if serializer2.is_valid():
                user = serializer.save()
                username = user.username
                teacher = serializer2.save(username)
                author = get_object_or_404(User, username=username)
                code = get_object_or_404(ActivationKeys, user=author)
                send_mail('Contact Form', 
                    'Ur activation key is {} link: https://uni30-5.unilearn.com.eg/activation/'.format(code.code),
                    settings.EMAIL_HOST_USER,
                    ['{}'.format(author.email)],
                    fail_silently=False)
            else:
                return Response({'error': serializer2.errors}, 403)
        else:
            return Response({'error': serializer.errors}, 403)

        return Response({'success': 'check your email: {}'.format(author.email)}, 201)
    elif request.method == 'GET':
        all_students = Student.objects.all()
        serializer = UpdateStudentWithActivation(all_students, many=True)
        return Response({'data': serializer.data}, 200)


@api_view(['PUT', 'DELETE'])
@teacher_role
def update_student(request, id, username):
    user = request.user
    student = get_object_or_404(Student, id=id)
    userStudent = User.objects.filter(name=username)[0]
    if request.method == 'PUT':
        serializer = UpdateStudentWithActivation(data=request.data, instance=student)
        if serializer.is_valid():
            new_serializer = serializer.save()
            return Response({'success': 'user updated successfully'}, 200)
        return Response({'error': serializer.errors}, 403)
    elif request.method == 'DELETE':
        student.delete()
        return Response({'success': 'user deleted successfully'}, 200)