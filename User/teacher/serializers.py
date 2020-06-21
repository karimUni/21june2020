from rest_framework import serializers
from rest_framework.response import Response
from User.models import User, Teacher, Subject, ClassRoom, HeadMaster, Student
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import random


class RegisterationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=150)
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'phone_number', 'role', 'address', 'avatar', 'first_name', 'last_name', 'name']
        read_only_fields = ['id', 'phone_number', 'address', 'first_name', 'last_name', 'avatar', 'username']

    def save(self):
        user = User(
            email = self.validated_data['email'],
            role = self.validated_data['role'],
        )
        password = ''
        for i in range(0, 9):
            password += str(int(random.random()*10))
        name = self.validated_data['name']
        fname = name.split(' ')[0]
        lname = name.split(' ')[1]
        user.set_fname(fname)
        user.set_lname(lname)
        user.set_name('{} {}'.format(fname, lname))
        username = '{}{}{}'.format(fname, str(int(random.random()*100)), lname)
        user.set_username_u(username)
        user.set_password(password)
        user.save()
        return user



class CreateTeacher(serializers.ModelSerializer):
    subject = serializers.CharField(style={'input_type' : 'text'}, max_length=100)
    class Meta:
        model = Teacher
        fields = ['id', 'uni_code', 'grade', 'level', 'subject', 'is_aproved']
        read_only_fields = ['id', 'uni_code', 'level', 'is_aproved']

    def save(self, xyz, **kwargs):
        user = get_object_or_404(User, username=xyz)
        teacher = Teacher(
            grade = self.validated_data['grade']
        )
        uni_code = 'khaled-international-secondary'
        # headmaster = get_object_or_404(HeadMaster, uni_code=uni_code)
        level = ''
        ownGrade = self.validated_data['grade']
        if ownGrade in range(1, 6):
            level = 'Primary'
        elif ownGrade in range(7, 9):
            level = 'Preparatory'
        else:
            level = 'Secondary'
            
        subject = self.validated_data['subject']
        try:
            ddm = Subject.objects.get(name=subject)
        except ObjectDoesNotExist:
            if user:
                user.delete()
            else:
                pass
            raise serializers.ValidationError({'subject': 'subject must be exist'})

        teacher.set_uni_code(uni_code)
        teacher.set_user(user)
        teacher.set_subject(ddm)
        teacher.set_level(level)
        teacher.save()
        return teacher