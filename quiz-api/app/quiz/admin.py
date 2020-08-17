from django.contrib import admin
import nested_admin

from quiz import models

# Django admin panel configuration for all model data
# Access django admin panel using localhost:8001/admin
# Based on these configurations we can add/edit/delete our model data using admin ui


class AnswerInline(nested_admin.NestedTabularInline):
    model = models.Answer
    extra = 4
    max_num = 4


class QuestionInline(nested_admin.NestedTabularInline):
    model = models.Question
    inlines = [AnswerInline, ]
    extra = 5


class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline, ]


class UserAnswerInline(admin.TabularInline):
    model = models.UserAnswer


class QuizTakerAdmin(admin.ModelAdmin):
    inlines = [UserAnswerInline, ]


admin.site.register(models.Quiz, QuizAdmin)
admin.site.register(models.Question)
admin.site.register(models.Answer)
admin.site.register(models.QuizTaker, QuizTakerAdmin)
admin.site.register(models.UserAnswer)
