# Contains all endpoints for quiz functionality
# Mapped url paths are directed to the corresponding endpoint here.

from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.db.models import Q
from quiz.models import Quiz, QuizTaker, Question, UserAnswer, Answer
from quiz.serializers import QuizDetailSerializer, MyQuizListSerializer, UserAnswerSerializer, \
    QuizResultSerializer
import random
from django.http import JsonResponse


# Endpoint to retrieve set of completed quizzes when a user clicks on History
class MyQuizListView(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = MyQuizListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Quiz.objects.filter(quiztaker__user=self.request.user, quiztaker__completed=True)
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            ).distinct()

        return queryset


# Endpoint to generate a new quiz or retrieve in-progress quiz when a user clicks play
class QuizDetailView(generics.RetrieveAPIView):
    serializer_class = QuizDetailSerializer
    permission_classes = [
        permissions.IsAuthenticated

    ]

    def get(self, *args, **kwargs):
        slug = self.request.GET.get("slug")
        queryset = Quiz.objects.filter(quiztaker__user=self.request.user, quiztaker__completed=False)

        if len(queryset) > 0:
            quiz = queryset[0]
        else:
            try:
                quiz = random.choice(Quiz.objects.exclude(quiztaker__user=self.request.user))
            except IndexError:
                return JsonResponse({}, status=204)
        last_question = None
        obj, created = QuizTaker.objects.get_or_create(user=self.request.user, quiz=quiz)
        if created:
            for question in Question.objects.filter(quiz=quiz):
                UserAnswer.objects.create(quiz_taker=obj, question=question)
        else:
            last_question = UserAnswer.objects.filter(quiz_taker=obj, answer__isnull=False)
            if last_question.count() > 0:
                last_question = last_question.last().question.id
            else:
                last_question = None

        return Response({'quiz': self.get_serializer(quiz, context={'request': self.request}).data,
                         'last_question_id': last_question})


# Endpoint to retrieve quiz information.
class QuizInfoView(generics.RetrieveAPIView):
    serializer_class = QuizDetailSerializer
    permission_classes = [
        permissions.IsAuthenticated

    ]

    def get(self, *args, **kwargs):
        slug = self.kwargs["slug"]
        quiz = get_object_or_404(Quiz, slug=slug)

        return Response({'quiz': self.get_serializer(quiz, context={'request': self.request}).data})


# Endpoint to save a user's answer to a question
class SaveUserAnswer(generics.UpdateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def patch(self, request, *args, **kwargs):
        quiztaker_id = request.data['quiztaker']
        question_id = request.data['question']
        answer_id = request.data['answer']

        question = get_object_or_404(Question, id=question_id)
        answer = get_object_or_404(Answer, id=answer_id)
        quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)

        if quiztaker.completed:
            return Response({
                "message": "This quiz is already complete. you can't answer any more questions"},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        obj = get_object_or_404(UserAnswer, quiz_taker=quiztaker, question=question)
        obj.answer = answer
        obj.save()

        return Response(self.get_serializer(obj).data)


# Endpoint to submit final quiz
class SubmitQuizView(generics.GenericAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def post(self, request, *args, **kwargs):
        # Data submitted in post body
        quiztaker_id = request.data['quiztaker']
        question_id = request.data['question']
        answer_id = request.data['answer']

        # Take the quiztaker object and the final question (submission happens when final question is answered)
        quiztaker = get_object_or_404(QuizTaker, id=quiztaker_id)
        question = get_object_or_404(Question, id=question_id)

        quiz = Quiz.objects.get(slug=self.kwargs['slug'])

        # Send error response if quiz is already completed.
        if quiztaker.completed:
            return Response({
                'message': 'This quiz has already been completed.'},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

        # Save the final answer
        if answer_id is not None:
            answer = get_object_or_404(Answer, id=answer_id)
            obj = get_object_or_404(UserAnswer, quiz_taker=quiztaker, question=question)
            obj.answer = answer
            obj.save()

        quiztaker.completed = True
        correct_answers = 0

        # Loop to verify quiz answers
        for user_answer in UserAnswer.objects.filter(quiz_taker=quiztaker):
            answer = Answer.objects.get(question=user_answer.question, is_correct=True)
            if user_answer.answer == answer:
                correct_answers += 1

        quiztaker.score = int(correct_answers / quiztaker.quiz.question_set.count() * 100)
        quiztaker.save()

        return Response(self.get_serializer(quiz).data)