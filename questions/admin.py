from django.contrib import admin

from .models import Question, Choice, TriviaFeedback, TransitFeedback

admin.site.register([Question, Choice, TriviaFeedback, TransitFeedback])
