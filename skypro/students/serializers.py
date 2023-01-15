from rest_framework import serializers
from students.models import Resume
from django.contrib.auth.models import User


class ResumeSerializers(serializers.ModelSerializer):
    
    class Meta:
       model = Resume
       fields = '__all__'
       
class UserLoginSerializer(serializers.ModelSerializer):
    
    class Meta:
       model = User
       fields = ('username', 'password')
     