from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Resume(models.Model):
    """
    Модель записи резюме студента
    """   
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', 
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
        )
    
    status = models.CharField(max_length=30, blank=False, null=True, default='status')
    grade = models.CharField(max_length=30, blank=False, null=True, default='grade')
    speciality = models.CharField(max_length=30, blank=False, null=True, default='speciality')
    salary = models.CharField(max_length=30, blank=False, null=True, default='salary')
    education = models.CharField(max_length=30, blank=False, null=True, default='education')
    experience = models.CharField(max_length=30, blank=False, null=True, default='experience')
    portfolio = models.CharField(max_length=30, blank=False, null=True, default='portfolio')
    title = models.CharField(max_length=30, blank=False, null=True, default='title')
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(default='email@mail.com')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Резюме {self.title}, портфолио {self.portfolio}, ..."
