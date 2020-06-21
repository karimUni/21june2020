from rest_framework import serializers
from django.shortcuts import get_object_or_404
from drf_writable_nested.serializers import WritableNestedModelSerializer
from User.models import User, HeadMaster, Teacher, Student, Parent, Subject, ClassRoom


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'username',  'role',  'password']
    def save(self):
        # user = User(
        #     email = self.validated_data['email'],
        #     username = self.validated_data['username'],
        #     role = self.validated_data['role'],
        
        # )
        # password = self.validated_data['password']
        # user.set_password(password)
        # user.save()
        user = User.objects.create_user(**self.validated_data)
        return user

class TeacherSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Teacher
        fields = ('id','uni_code','grade','level' ,'user','subject','class_rooms')

class StudentSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ('id', 'uni_code', 'grade', 'level', 'class_room','subjects','user')
        read_only  = ['id']

class ParentSerializer(WritableNestedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Parent
        fields = ('id', 'uni_code', 'user',)
        read_only  = ['id']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id','name','level' , 'grade',]
        read_only = ['id']

class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = ['id', 'number', 'grade','level']
        read_only = ['id']