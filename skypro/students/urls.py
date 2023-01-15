
from django.urls import path, include
from rest_framework import routers
from students.views import ResumeViewSet, LoginAPIView, LogoutAPIView



router = routers.DefaultRouter()
router.register('resume', ResumeViewSet, basename='resume')
urlpatterns = router.urls

urlpatterns += [
    path('login/', LoginAPIView.as_view(), name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
]