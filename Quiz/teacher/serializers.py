# Quiz serializers to Create New Quiz# Notes this serializer.py only for teacher to create Quiz

from rest_framework import serializers
from rest_framework.response import Response
from Quiz.models import Quiz
from Question.models import Question, MCQ, TR, Rate
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import random
from User.models import Subject, Teacher, Student
from Report.models import ReportStudent


#serializer for create new Quiz
class CreateNewQuiz(serializers.ModelSerializer):
    
    class Meta:
        model = Quiz
        fields = ['quiz_id' ,'quiz_headline', 'quiz_grade', 'quiz_real_time', 'quiz_setion_time', 'quiz_launch_time', 'quiz_is_launched']
        read_only_fields = ['quiz_id', 'quiz_real_time', 'quiz_setion_time', 'quiz_launch_time', 'quiz_is_launched']

    def save(self, subject, author, quiz_id, **kwargs):
        quiz = Quiz(
            quiz_headline = self.validated_data['quiz_headline'],
            quiz_grade = self.validated_data['quiz_grade']
        )

        quiz_subject = get_object_or_404(Subject, name=subject)
        if (not quiz_subject):
            raise serializers.ValidationError({'subject': 'subject not exist'})
        quiz_author = get_object_or_404(Teacher, user=author)
        if (not quiz_author):
            raise serializers.ValidationError({'author': 'author not provided'})
        
        quiz.set_quiz_id(quiz_id)
        quiz.set_quiz_subject(quiz_subject)
        quiz.set_quiz_author(quiz_author)
        quiz.save()

        return quiz


class CreateQuestion(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = ['id', 'question_id', 'question_type', 'question_real_time', 'question_grade', 'question_topic', 'question_level', 'question_author', 'question_creation_time']
        read_only_fields  = ['id','question_id' , 'question_author', 'question_level', 'question_real_time', 'question_creation_time']

    def save(self, author, subject, **kwargs):
        qustion = Question(
            question_type = self.validated_data['question_type'],
            question_grade = self.validated_data['question_grade'],
            question_topic = self.validated_data['question_topic'],
        )
        level = ''
        q_g = self.validated_data['question_grade']
        if int(q_g) in range(1, 6):
            level = 'Primarty'
        elif  int(q_g) in range(7, 9):
            level = 'Preparatory'
        else:
            level = 'Secondary'
        SEKRET_ID = int(random.random() * 999999)
        question_author = get_object_or_404(Teacher, user=author)
        if (not question_author):
            raise serializers.ValidationError({'user': 'user not exist'})
        question_subject = get_object_or_404(Subject, name=subject)
        if (not question_subject):
            raise serializers.ValidationError({'subject': 'subject not exist'})

        qustion.set_question_author(question_author)
        qustion.set_question_subject(question_subject)
        qustion.set_question_id(SEKRET_ID)
        qustion.set_level(level)
        qustion.save()

        return qustion

class CreateMCQ(serializers.ModelSerializer):

    class Meta:
        model = MCQ
        fields = ['question', 'question_head', 'question_head_avatar', 'question_body', 'question_answer', 'choice_A', 'choice_B', 'choice_C', 'choice_D']
        read_only_fields = ['question']

    def save(self, question, **kwargs):
        mcq = MCQ(
            question_head = self.validated_data['question_head'],
            question_body = self.validated_data['question_body'],
            choice_A = self.validated_data['choice_A'],
            choice_B = self.validated_data['choice_B'],
            choice_C = self.validated_data['choice_C'],
            choice_D = self.validated_data['choice_D'],
            question_answer = self.validated_data['question_answer'],
            question_head_avatar = self.validated_data['question_head_avatar'],
        )

        if (not question):
            raise serializers.ValidationError({'question': 'question not exist'})
        mcq.set_question(question)
        q_t = int(len(self.validated_data['question_head'])) + int(len(self.validated_data['question_body'])) + int(len(self.validated_data['choice_A'])) + int(len(self.validated_data['choice_B'])) + int(len(self.validated_data['choice_C'])) + int(len(self.validated_data['choice_D']))
        question.set_time(q_t)
        mcq.save()

        return mcq

class CreateTR(serializers.ModelSerializer):

    class Meta:
        model = TR
        fields = ['question', 'question_body', 'question_answer']
        read_only_fields = ['question']

    def save(self, question, **kwargs):
        tr = TR(
            question_body = self.validated_data['question_body'],
            question_answer = self.validated_data['question_answer']
        )

        if (not question):
            raise serializers.ValidationError({'question': 'question not exist'})
        tr.set_question(question)
        q_t = int(len(self.validated_data['question_body'])) + int(len(self.validated_data['question_answer']))
        question.set_time(q_t)
        tr.save()

        return tr


class CreateReportForStudent(serializers.ModelSerializer):

    class Meta:
        model = ReportStudent
        fields = ['report_id', 'report_student', 'report_creator', 'report_subject']
        read_only_fields = ['report_student', 'report_creator', 'report_subject']

    def save(self, report_student, report_creator, **kwargs):

        report = ReportStudent(
            report_id = self.validated_data['report_id'],
        )
        if (not report_student or not report_creator):
            raise serializers.ValidationError({'detail': 'data messing'})
        student = get_object_or_404(Student, id=int(report_student))
        teacher = get_object_or_404(Teacher, user=report_creator)
        subject = teacher.subject

        report.set_author(teacher)
        report.set_reciver(student)
        report.set_subject(subject)
        report.save()
        return report

        # not completed yet


class CreateRate(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ['stars', 'comment', 'question', 'author', 'subject', 'creation_time']
        read_only_fields = ['question', 'author', 'subject', 'creation_time']

    def save(self, question, author, subject, **kwargs):

        rate = Rate(
            stars = self.validated_data['stars'],
            comment = self.validated_data['comment']
        )
        if (not question or not author):
            raise serializers.ValidationError({'detail': 'data messing'})
        rate.set_question(question)
        rate.set_author(author)
        rate.set_subject(subject)
        rate.save()

        return rate