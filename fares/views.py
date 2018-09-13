import json

from datetime import datetime, date

from django.db import connections

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Fare


class AddFareView(APIView):
    def post(self, request):
        json_data = json.loads(request.body)

        fare = Fare()
        fare.stop_to = json_data['stop_to']
        fare.stop_from = json_data['stop_from']
        fare.amount = json_data['amount']
        fare.stop_from_id = json_data['stop_from_id']
        fare.route_id = json_data['route_id']
        fare.stop_to_id = json_data['stop_to_id']
        fare.weather = json_data['weather']
        fare.traffic_jam = json_data['traffic_jam']
        fare.demand = json_data['demand']
        fare.air_quality = json_data['air_quality']
        fare.peak = json_data['peak']
        fare.travel_time = json_data['travel_time']
        fare.crowd = json_data['crowd']
        fare.safety = json_data['safety']
        fare.drive_safety = json_data['drive_safety']
        fare.music = json_data['music']
        fare.internet = json_data['internet']
        fare.user = request.user
        fare.save()

        return Response({"success": True})


class BudgetFareView(APIView):
    def get(self, request):
        try:
            cursor = connections['default'].cursor()
            cursor.execute("SELECT travel_time , amount "
                           "FROM fares_fare "
                           "WHERE user_id = {}".format(request.user.id))
            columns = [column[0] for column in cursor.description]
            fares = []
            for row in cursor.fetchall():
                fares.append(dict(zip(columns, row)))

            for item in fares:
                travel_time = datetime.strptime(item['travel_time'], "%Y-%m-%d %H:%M:%S")
                hour = int(str(travel_time.time())[0:2])
                travel_times = [6, 9, 12, 15, 18]
                closest = None

                item['week'] = travel_time.isocalendar()[1]

                for i in travel_times:
                    if not closest or (abs(i - closest) > abs(i - hour)):
                        closest = i

                if closest:
                    temp_time = datetime.strptime(item['travel_time'], "%Y-%m-%d %H:%M:%S").replace(hour=closest,
                                                                                                    minute=00,
                                                                                                    second=00)
                    item['travel_time'] = temp_time.time()

            return Response({"success": True, "result": fares})
        except Exception as e:
            return Response({"success": False, "result": str(e)})