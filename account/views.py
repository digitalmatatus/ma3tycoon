from django.contrib.auth import get_user_model, authenticate, update_session_auth_hash

from rest_framework.views import APIView
from rest_framework.response import Response


class Settings(APIView):
    def get(self, request):
        try:
            user_details = {
                'username': request.user.username,
                'email': request.user.email
            }
            return Response({"success": True, "result": user_details})
        except Exception as e:
            return Response({"success": False, "result": str(e)})

    def post(self, request):
        user_id = request.user.id

        try:
            User = get_user_model()
            user = User.objects.get(id=user_id)

            user.username = request.data['username']
            user.email = request.data['email']
            user.save()
            return Response({"success": True})
        except Exception as e:
            return Response({"success": False, "result": str(e)})


class Password(APIView):
    def post(self, request):
        username = request.user.username

        current_password = request.data['current_password']
        new_password = request.data['new_password']
        confirm_password = request.data['confirm_password']
        if new_password is not confirm_password:
            return Response({"success": False, "result": "The 2 passwords do not match"})

        user = authenticate(username=username, password=current_password)
        if user:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            return Response({"success": True})
        else:
            return Response({"success": False, "description": "Existing password mismatch"})