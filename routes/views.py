from django.db import connections

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class RoutesView(APIView):
    def get(self, request):
        cursor = connections['gtfs'].cursor()
        cursor.execute("SELECT route_id, short_name FROM route")
        columns = [column[0] for column in cursor.description]
        routes = []
        for row in cursor.fetchall():
            routes.append(dict(zip(columns, row)))

        return Response({"success": True, "result": routes})
