import json

from django.db import connections

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class RoutesView(APIView):
    def __init__(self):
        self.cursor = connections['gtfs'].cursor()

    def get(self, request):
        try:
            self.cursor.execute("SELECT route_id, short_name FROM route")
            columns = [column[0] for column in self.cursor.description]
            routes = []
            for row in self.cursor.fetchall():
                routes.append(dict(zip(columns, row)))

            return Response({"success": True, "result": routes})
        except Exception as e:
            return Response({"success": False, "result": str(e)})

    def post(self, request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))['data']
            route = json_data['route']

            self.cursor.execute(" SELECT ST_AsText(geometry), ST_AsText(ST_Centroid(geometry)) "
                                " FROM route "
                                " WHERE route_id = '{}'".format(route))
            result = self.cursor.fetchone()
            route_wkt = result[0]
            route_center = result[1]

            self.cursor.execute(" SELECT s.stop_id, s.name, ST_AsText(s.point) AS position "
                                " FROM route r"
                                " JOIN trip t ON(t.route_id=r.id)"
                                " JOIN stop_time s_t ON(s_t.trip_id=t.id)"
                                " JOIN stop s ON(s.id=s_t.stop_id)"
                                " WHERE r.route_id = '{}'".format(route))
            columns = [column[0] for column in self.cursor.description]
            stops = []
            for row in self.cursor.fetchall():
                stops.append(dict(zip(columns, row)))

            return Response({"success": True, "result": {
                    "route_center": route_center,
                    "route_wkt": route_wkt,
                    "stops": stops,
                }})
        except Exception as e:
            return Response({"success": False, "result": str(e)})
