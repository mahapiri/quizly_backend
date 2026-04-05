from django.urls import path

from quizzes_app.api.views import QuizzesView

urlpatterns = [
    path("", QuizzesView.as_view(), name="quizzes"),
]