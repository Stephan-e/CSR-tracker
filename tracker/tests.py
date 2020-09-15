from django.test import Client, TestCase

# Create your tests here.
from django.urls import reverse

from .models import Company

class CompanyTests(TestCase):
    def setUp(self):
        self.company = Company.objects.create(
        name='Bad Company',
        description='This is a bad company.',
        )

    def test_company_listing(self):
        self.assertEqual(f'{self.company.name}', 'Bad Company')
        self.assertEqual(f'{self.company.description}', 'This is a bad company.')

    def test_company_list_view(self):
        response = self.client.get(reverse('company_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bad Company')
        self.assertTemplateUsed(response, 'tracker/company.html')

    def test_company_detail_view(self):
        response = self.client.get(self.company.get_absolute_url())
        no_response = self.client.get('/tracker/company/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'Bad Company')
        self.assertTemplateUsed(response, 'tracker/company_detail.html')