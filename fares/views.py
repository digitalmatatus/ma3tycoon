import time
from datetime import datetime, date

from django.db import connections

from rest_framework.views import APIView
from rest_framework.response import Response


class BudgetView(APIView):
    def get(self, request):
        try:
            cursor = connections['gtfs'].cursor()
            cursor.execute("SELECT travel_time , amount "
                           "FROM multigtfs_newfare "
                           "WHERE "
                                "travel_time::DATE >= date_trunc('week', CURRENT_TIMESTAMP - interval '1 week')")
            columns = [column[0] for column in cursor.description]
            fares = []
            for row in cursor.fetchall():
                fares.append(dict(zip(columns, row)))

            for item in fares:
                week = '2'
                travel_time = datetime.strptime(item['travel_time'], "%Y-%m-%d %H:%M:%S")
                hour = int(str(travel_time.time())[0:2])
                travel_times = [6, 9, 12, 15, 18]
                closest = None

                if travel_time.isocalendar()[1] == date.today().isocalendar()[1]:
                    week = '1'

                for i in travel_times:
                    if not closest or (abs(i - closest) > abs(i - hour)):
                        closest = i

                if closest:
                    temp_time = datetime.strptime(item['travel_time'], "%Y-%m-%d %H:%M:%S").replace(hour=closest,
                                                                                                    minute=00,
                                                                                                    second=00)
                    item['travel_time'] = temp_time.time()
                item['week'] = week

            return Response({"success": True, "result": fares})
        except Exception as e:
            return Response({"success": False, "result": str(e)})