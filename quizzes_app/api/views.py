
from rest_framework import generics

from quizzes_app.api.serializers import QuizzesCreateSerializer, QuizzesSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from quizzes_app.models import Quiz


class QuizzesView(generics.CreateAPIView):
    serializer_class = QuizzesCreateSerializer
    permission_classes = [AllowAny]
    queryset = Quiz.objects.all()

