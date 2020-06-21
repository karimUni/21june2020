from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .models import Question , MCQ , TR

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id','question_type',  'question_grade', 'question_topic']

class MCQSerializer(serializers.ModelSerializer):
    class Meta:
        model = MCQ
        fields = ['question','question_head','question_body','choice_A' ,'choice_B','choice_C','choice_D','question_answer']