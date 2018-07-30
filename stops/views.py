from django.db import connections

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class StopsView(APIView):
    def __init__(self):
        self.cursor = connections['gtfs'].cursor()

    def get(self, request):
        try:
            return Response({"success": True, "result": self.get_stops()})
        except Exception as e:
            return Response({"success": False, "result": list(e)})

    def get_stops(self):
        self.cursor.execute("SELECT stop_id, name, ST_AsText(point) AS position FROM stop")
        columns = [column[0] for column in self.cursor.description]
        stops = []
        for row in self.cursor.fetchall():
            stops.append(dict(zip(columns, row)))
        return stops
