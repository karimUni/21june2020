from rest_framework import serializers
from rest_framework.response import Response
from Quiz.models import Quiz, Answers
from Question.models import Question, MCQ, TR
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
import random
from User.models import Subject, Student, ClassRoom


class CreateNewAnswer(serializers.ModelSerializer):
    class Meta:
        model = Answers
        fields = ['amswers_author', 'answers_points' ,'answer', 'time_to_answer', 'answers_quiz', 'answers_questions', 'answer_grade', 'answer_subject']
        read_only_fields = ['answers_points', 'answer_grade', 'answer_subject', 'amswers_author']

    def save(self, amswers_author, answer_grade, answer_subject, answers_points, **kwargs):
        answer = Answers(
            answer = self.validated_data['answer'],
            time_to_answer = self.validated_data['time_to_answer'],
            answers_quiz = self.validated_data['answers_quiz'],
            answers_questions = self.validated_data['answers_questions']
        )
        answer.set_amswers_author(amswers_author)
        answer.set_answer_subject(answer_subject)
        answer.set_answer_grade(answer_grade)
        answer.set_answers_points(answers_points)

        answer.save()

        return answer


