import json

from django.db import connections
from django.contrib.gis.geos import Point

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Question, Choice, TriviaFeedback, TransitFeedback, LeaderBoard


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


class TransitQuestionsView(APIView):
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


class LeaderBoardView(APIView):
    def get(self, request):
        try:
            cursor = connections['default'].cursor()
            cursor.execute("SELECT "
                           "u.username,"
                           " COALESCE(l.trivia_points,0) AS trivia,"
                           " COALESCE(l.transit_points,0) AS transit,"
                           " (l.trivia_points + l.transit_points) AS total"
                           " FROM questions_leaderboard l"
                           " JOIN auth_user AS u ON(u.id=l.user_id)"
                           " ORDER BY total DESC")
            columns = [column[0] for column in cursor.description]
            leaderboard = []
            for row in cursor.fetchall():
                leaderboard.append(dict(zip(columns, row)))
            cursor.execute("SELECT "
                           " COALESCE(trivia_points,0) AS trivia,"
                           " COALESCE(transit_points,0) AS transit,"
                           " (trivia_points + transit_points) AS total"
                           " FROM questions_leaderboard WHERE user_id = {}"
                           " ORDER BY total DESC".format(request.user.id))
            columns = [column[0] for column in cursor.description]
            details = cursor.fetchone() or []
            my_score = dict(zip(columns, details))

            return Response({"success": True, "leaderboard": leaderboard, "my_score": my_score})
        except Exception as e:
            return Response({"success": False, "result": str(e)})

