from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import test, status
from rest_framework.test import APIClient
from quiz.models import Quiz, QuizTaker
from quiz.serializers import QuizDetailSerializer, MyQuizListSerializer

QUIZ_DETAIL_URL = reverse('quiz:quizzes')
MY_QUIZ_LIST_URL = reverse('quiz:myquizzes')


#  Create a sample quiz
def sample_quiz(**params):
    defaults = {
        'name': 'sample quiz',
        'description': 'sample quiz description',
        'slug': 'sample-quiz',
        'roll_out': True,
        'timestamp': '2020-08-14T03:06:31.107Z',
    }
    defaults.update(params)

    return Quiz.objects.create(**defaults)


def sample_quiz_taker(user, quiz, **params):
    QuizTaker.objects.create(user=user, quiz=quiz)


# Test unauthorized access to the api
class PublicQuizApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(QUIZ_DETAIL_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# Test authenticated access to the api
class PrivateQuizApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@test.com',
            'test'
        )
        self.client.force_authenticate(self.user)

    # Test retrieving my quiz list
    def test_retrieve_my_quizzes(self):
        quiz_one = sample_quiz(name='Sample Quiz 1')
        quiz_two = sample_quiz(name='Sample Quiz 2')
        sample_quiz_taker(self.user, quiz_one)
        sample_quiz_taker(self.user, quiz_two)

        res = self.client.get(MY_QUIZ_LIST_URL)

        my_quizzes = Quiz.objects.all()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
