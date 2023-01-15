import json
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from students.models import Resume
from students.serializers import ResumeSerializers


resume_data = {
            'id':1,
            'status': '13',
            'grade': 'grade',
            'speciality': 'speciality',
            'salary': 'salary',
            'education': 'education',
            'experience': 'experience',
            'portfolio': 'portfolio',
            'title': 'title',
            'phone': 'phone',
            'email': 'email',
}


class AddArticlePageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create(
            username='username_1',
            first_name='first_name_1',
            last_name='last_name_1',
        )
        user1.set_password('11111111')
        user1.save()
        user = User.objects.create(
            username='username_2',
            first_name='first_name_2',
            last_name='last_name_2',
        )
        user.set_password('11111111')
        user.save()
        
        resume = Resume.objects.create(
            **resume_data, owner = user
        )
        resume.save()

    def test_patch_resume_success(self):
        self.client.login(username='username_2', password='11111111')
        data_to_patch = json.dumps({
            'status': 'status 2',
            'grade': 'not graded',
            'speciality': 'technical',
            'salary': 'big salary',
            'email': 'good@email.com',
            })
        
        response = self.client.patch(
            reverse(
                'resume-detail',
                kwargs={'pk': 1,},
            ),
            data_to_patch,
            content_type='application/json'
        )
        
        # print(response.__dict__)
        self.assertContains(response, 'not graded')
        self.assertContains(response, 'technical')
        self.assertContains(response, 'big salary')
        self.assertContains(response, 'status 2')
        self.assertContains(response, 'good@email.com')
        self.assertEqual(response.status_code, 200)

    def test_patch_resume_bad_email(self):
        self.client.login(username='username_2', password='11111111')
        data_to_patch = json.dumps({
            'email': 'bad email',
            'phone': 'bad phone',
            })
        
        response = self.client.patch(
            reverse(
                'resume-detail',
                kwargs={'pk': 1,},
            ),
            data_to_patch,
            content_type='application/json'
        )
        self.assertEqual(str(response.data['email'][0]), 'Enter a valid email address.')
        self.assertEqual(
            str(response.data['phone'][0]), 
            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
        self.assertEqual(response.status_code, 400)

    def test_patch_resume_not_login(self):
        response = self.client.patch(
            reverse(
                'resume-detail',
                kwargs={'pk': 1,},
            ),
        )
        self.assertEqual(response.status_code, 302)


    def test_patch_resume_other_owner(self):
        self.client.login(username='username_1', password='11111111')
        response = self.client.patch(
            reverse(
                'resume-detail',
                kwargs={'pk': 1,},
            ),
        )
        self.assertEqual(response.status_code, 400)

    def test_patch_resume_empty(self):
        self.client.login(username='username_2', password='11111111')
        response = self.client.patch(
            reverse(
                'resume-detail',
                kwargs={'pk': 2,},
            ),
        )
        self.assertEqual(response.status_code, 404)

    def test_get(self):
        response = self.client.get(
            reverse(
                'resume-detail',
                kwargs={'pk': 1,},
            ),
        )
        
        for item in resume_data:
            self.assertContains(response, item)
        self.assertEqual(response.status_code, 200)

    def test_get_empty(self):
        response = self.client.get(
            reverse(
                'resume-detail',
                kwargs={'pk': 2,},
            ),
        )
        
        self.assertEqual(response.status_code, 404)
    