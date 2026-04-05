from rest_framework import serializers

from quizzes_app.models import Quiz

class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_title = serializers.CharField(max_length=255)
    question_options = serializers.JSONField()
    answer = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class QuizzesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    video_url = serializers.URLField(max_length=255, required=False)
    questions = QuestionSerializer(many=True, read_only=True)

class QuizzesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['url']