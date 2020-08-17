from quiz.models import Quiz, QuizTaker, Question, Answer, UserAnswer
from rest_framework import serializers
# serializers map to an endpoint or a model. Transforms data to JSON response
# eg: AnswerSerializer transforms Answer model data
# eg: QuizDetailSerializer builds response data for QuizDetailView endpoint


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ["id", "question", "label", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    # Attributes that are outputted by this serializer
    answer_set = AnswerSerializer(many=True)
    useranswer_percent = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = "__all__"

    # Custom attribute to calculate percentage of users who has answered this quiz correctly
    def get_useranswer_percent(self, obj):
        try:
            userAnswers = UserAnswer.objects.filter(question_id=obj.id)
            correct_answer_id = Answer.objects.filter(question_id=obj.id, is_correct=True)[0].id
            correct_answer_count = 0
            total_answered = 0

            for userAnswer in userAnswers:
                if userAnswer.answer:
                    total_answered += 1
                    if correct_answer_id == userAnswer.answer.id:
                        correct_answer_count += 1

            return (correct_answer_count/total_answered)*100

        except UserAnswer.DoesNotExist:
            return None
        except ZeroDivisionError:
            return None


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = "__all__"


class MyQuizListSerializer(serializers.ModelSerializer):
    completed = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    questions_count = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    threshold_rate = serializers.SerializerMethodField()  # Percentage of users who has over 7 points for this quiz

    class Meta:
        model = Quiz
        fields = ["id", "name", "description", "slug", "questions_count", "completed", "score", "progress",
                  "threshold_rate"]
        read_only_fields = ["questions_count", "completed", "progress"]

    # Set of functions to derive custom attributes defined above
    def get_completed(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            return quiztaker.completed
        except QuizTaker.DoesNotExist:
            return None

    def get_progress(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if not quiztaker.completed:
                questions_answered = UserAnswer.objects.filter(quiz_taker=quiztaker, answer__isnull=False).count()
                total_questions = obj.question_set.all().count()
                return int(questions_answered / total_questions)
            return None
        except QuizTaker.DoesNotExist:
            return None

    def get_questions_count(self, obj):
        return obj.question_set.all().count()

    def get_score(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            if quiztaker.completed == True:
                return quiztaker.score
            return None
        except QuizTaker.DoesNotExist:
            return None

    # Calculate percentage of users who has taken over 7 for this quiz
    def get_threshold_rate(self, obj):
        try:
            quiztakers = QuizTaker.objects.filter(quiz=obj)
            over_threshold_count = 0
            total_takers = len(quiztakers)
            for quiztaker in quiztakers:
                if quiztaker.completed and quiztaker.score >= 70:
                    over_threshold_count += 1

            return (over_threshold_count/total_takers) * 100
        except QuizTaker.DoesNotExist:
            return None


# Serializer for the QuizTaker model
class QuizTakerSerializer(serializers.ModelSerializer):
    useranswer_set = UserAnswerSerializer(many=True)

    class Meta:
        model = QuizTaker
        fields = "__all__"


# Serializer for quiz detail endpoint
class QuizDetailSerializer(serializers.ModelSerializer):
    quiztakers_set = serializers.SerializerMethodField()
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = "__all__"

    def get_quiztakers_set(self, obj):
        try:
            quiz_taker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            serializer = QuizTakerSerializer(quiz_taker)
            return serializer.data
        except QuizTaker.DoesNotExist:
            return None


class QuizResultSerializer(serializers.ModelSerializer):
    quiztaker_set = serializers.SerializerMethodField()
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = "__all__"

    def get_quiztaker_set(self, obj):
        try:
            quiztaker = QuizTaker.objects.get(user=self.context['request'].user, quiz=obj)
            serializer = QuizTakerSerializer(quiztaker)
            return serializer.data

        except QuizTaker.DoesNotExist:
            return None