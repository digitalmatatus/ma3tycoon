import json
import random

from django.db import connections
from django.contrib.gis.geos import Point

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Question, Choice, TriviaFeedback, TransitFeedback, LeaderBoard


class TriviaQuestions(APIView):
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
            return Response({"success": False, "result": str(e)})

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            points_gained = 0
            for data in json_data['data']:
                choice_obj = Choice.objects.get(id=data['choice'])
                TriviaFeedback.objects.create(question=Question.objects.get(id=data['question']),
                                              choice=choice_obj, user=request.user)
                points_gained += choice_obj.points
            if LeaderBoard.objects.filter(user=request.user).first():
                board = LeaderBoard.objects.filter(user=request.user).first()
                board.trivia_points += board.transit_points + points_gained
                board.save()
            else:
                LeaderBoard.objects.create(user=request.user, trivia_points=points_gained)

            return Response({"success": True, "points_gained": points_gained})
        except Exception as e:
            return Response({"success": False, "result": str(e)})


class TransitQuestions(APIView):
    def __init__(self):
        self.POINTS_PER_TRANSIT_FEEDBACK = 10

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            points_gained = 0
            for data in json_data['data']:
                TransitFeedback.objects.create(stop=data['stop'], point=Point(float(data['longitude']), float(data['latitude'])),
                                               position_correct=data['position_correct'], user=request.user)
                points_gained += self.POINTS_PER_TRANSIT_FEEDBACK

            if LeaderBoard.objects.filter(user=request.user).first():
                board = LeaderBoard.objects.filter(user=request.user).first()
                board.transit_points += board.transit_points + points_gained
                board.save()
            else:
                LeaderBoard.objects.create(user=request.user, transit_points=points_gained)

            return Response({"success": True, "points_gained": points_gained})
        except Exception as e:
            return Response({"success": False, "result": str(e)})


class LeaderBoard(APIView):
    def get(self, request):
        try:
            cursor = connections['default'].cursor()
            cursor.execute("SELECT "
                           " u.username,"
                           " COALESCE(l.trivia_points,0) AS trivia,"
                           " COALESCE(l.transit_points,0) AS transit,"
                           " (l.trivia_points + l.transit_points) AS total,"
                           " rank() over (order by (l.trivia_points + l.transit_points) desc) as rank"
                           " FROM questions_leaderboard l"
                           " JOIN auth_user AS u ON(u.id=l.user_id)"
                           " ORDER BY total DESC")
            columns = [column[0] for column in cursor.description]
            leaderboard = []
            for row in cursor.fetchall():
                leaderboard.append(dict(zip(columns, row)))

            my_score = []
            for i in leaderboard:
                if i['username'] == request.user.username:
                    my_score.append(i)

                    break

            return Response({"success": True, "leaderboard": leaderboard, "my_score": my_score})
        except Exception as e:
            return Response({"success": False, "result": str(e)})


class Analysis(APIView):
    def get(self, request):
        try:
            cursor = connections['default'].cursor()

            cursor.execute("SELECT q.id, q.question_text, json_agg(json_build_object('id' , c.id, 'choice_text',"
                           " c.choice_text)) as choices FROM questions_question q INNER JOIN questions_choice c ON "
                           "(c.question_id = q.id) GROUP BY q.id, q.question_text")

            columns = [column[0] for column in cursor.description]
            result = []
            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))

            cursor.execute("SELECT choice_id, COUNT(choice_id) AS frequency FROM questions_triviafeedback GROUP BY choice_id")
            columns = [column[0] for column in cursor.description]
            aggregates = []
            for row in cursor.fetchall():
                aggregates.append(dict(zip(columns, row)))

            for choice_options in result:
                choices = choice_options['choices']
                for choice in choices:
                    for aggregate in aggregates:
                        if aggregate['choice_id'] == choice['id']:
                            choice['frequency'] = aggregate['frequency']
                            choice['color'] = "#%06x" % random.randint(0, 0xFFFFFF)

            return Response({"success": True, "result": result})
        except Exception as e:
            return Response({"success": False, "result": str(e)})