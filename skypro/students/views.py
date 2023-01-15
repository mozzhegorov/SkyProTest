from rest_framework import viewsets
from students.models import Resume
from students.serializers import ResumeSerializers
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from students.serializers import UserLoginSerializer
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from http import HTTPStatus


class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializers
    
    @method_decorator(login_required)
    def partial_update(self, request, *args, **kwargs):
        if self.get_object().owner != request.user:
            return Response(status=HTTPStatus.BAD_REQUEST)
        return super().partial_update(request, *args, **kwargs)
    

class LoginAPIView(APIView):
    """API View для авторизации."""

    def post(self, request):
        user = authenticate(request, **request.data)
        if user is not None:
            login(request, user)
            return Response(
                UserLoginSerializer(user).data,
                status=HTTPStatus.OK
            )
        return Response(status=HTTPStatus.BAD_REQUEST)


class LogoutAPIView(APIView):
    """API View для выхода из системы."""

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return Response(status=HTTPStatus.OK)

