import json

from django.db import connections
from django.contrib.gis.geos import Point

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Question, Choice, TriviaFeedback, TransitFeedback


class TriviaQuestionsView(APIView):
    def get(self, request):
        try:
            cursor = connections['default'].cursor()
            cursor.execute("SELECT q.id, q.question_text, json_agg(json_build_object('id' , c.id, 'choice_text',"
                           " c.choice_text)) as choices FROM questions_question q INNER JOIN questions_choice c ON "
                           "(c.question_id = q.id) GROUP BY q.id, q.question_text")
            columns = [column[0] for column in cursor.description]
            questions = []
            for row in cursor.fetchall():
                questions.append(dict(zip(columns, row)))

            return Response({"success": True, "result": questions})
        except Exception as e:
            return Response({"success": False, "result": e})

    def post(self, request):
        try:
            json_data = json.loads(request.body)
            for data in json_data['data']:
                TriviaFeedback.objects.create(question=Question.objects.get(id=data['question']),
                                              choice=Choice.objects.get(id=data['choice']), user=request.user)
            return Response({"success": True})
        except Exception as e:
            return Response({"success": False, "result": e})


class TransitQuestionsView(APIView):
    def post(self, request):
        try:
            json_data = json.loads(request.body)
            for data in json_data['data']:
                TransitFeedback.objects.create(stop=data['stop'], point=Point(data['longitude'], data['latitude']),
                                               position_correct=data['position_correct'], user=request.user)

            return Response({"success": True})
        except Exception as e:
            return Response({"success": False, "result": e})
