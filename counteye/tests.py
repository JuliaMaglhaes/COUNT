from django.test import TestCase
from django.contrib.auth.models import User
from counteye.models import Count, Category

class TesteCount(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass