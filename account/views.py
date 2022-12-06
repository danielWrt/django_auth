from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer
from .models import User


class RegisterUserView(APIView):
    
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
    
        return Response('Successfully registration')


class DeleteUserView(APIView):

    def delete(self, request, email):
        user = get_object_or_404(User, email=email)

        if user.is_staff or user != request.user:
            return Response(status=403) # запрещаем
        
        user.delete()

        return Response(status=204)


@api_view(['GET'])
def check_auth(request):
    if request.user.is_authenticated:
        return Response(status=200)

    return Response(status=401)
