from django.db import connections

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class StopsView(APIView):
    def get(self, request):
        cursor = connections['gtfs'].cursor()
        cursor.execute("SELECT stop_id, name FROM stop")
        columns = [column[0] for column in cursor.description]
        stops = []
        for row in cursor.fetchall():
            stops.append(dict(zip(columns, row)))

        return Response({"success": True, "result": stops})
