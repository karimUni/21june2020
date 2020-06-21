from rest_framework import serializers
from User.models import Teacher , Subject , Student , ClassRoom
from Quiz.models import Quiz , Answers
from django.shortcuts import get_object_or_404
from User.models import User


class getAllStudents(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='name',
        queryset=User.objects.all())
    class Meta:
        model = Student
        fields = ['id', 'level', 'class_room', 'groub', 'user']
        read_only_fields = ['id', 'level', 'class_room', 'groub', 'user']


class getAllClasses(serializers.ModelSerializer):
    quiz_class_room = serializers.SerializerMethodField()
    quiz_questions = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ['id', 'quiz_id', 'quiz_headline', 'quiz_grade', 'quiz_class_room', 'quiz_questions']
        read_only_fields = ['id', 'quiz_id', 'quiz_headline', 'quiz_grade', 'quiz_class_room', 'quiz_questions']

    def get_quiz_questions(self, obj):
        return obj.quiz_questions.all().count()
    
    def get_quiz_class_room(self, obj):
        return obj.quiz_class_room.all()[0].name














# class QuizesSerilizer(serializers.ModelSerializer):
#     questions_count = serializers.SerializerMethodField()

#     def get_questions_count(self,obj):
#         if obj:
#             return obj.quiz_questions.all().count()

#     class Meta:
#         model = Quiz
#         fields = ('quiz_id','questions_count','quiz_creation_time')



# class ClassRoomSerilizer(serializers.ModelSerializer):
#     quiz = QuizesSerilizer(source='quiz_class', many=True)
#     student_count = serializers.SerializerMethodField()
    
#     def get_student_count(self,obj):
#         if obj:
#             return obj.student_class.all().count()

#     class Meta:
#         model = ClassRoom
#         fields = ('id','name','quiz','student_count')
