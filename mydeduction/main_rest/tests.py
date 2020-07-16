from django.test import TestCase
from main_rest.models import DSet

# Create your tests here.
class Test1(TestCase):
    ''' Testing simple set deduction. '''

    @classmethod
    def setUpTestData(cls):
        # creating models
        xiaoming = DSet.objects.create(name='xiaoming')
        human = DSet.objects.create(name='human')
        primate = DSet.objects.create(name='primate')
        # linking
        xiaoming.save()
        xiaoming.parents.add(human)
        human.save()
        human.parents.add(primate)
        primate.save()
        # recording vars
        cls.human = human
        cls.xiaoming = xiaoming
        cls.primate = primate

    def test_deduce(self,):
        xiaoming = self.xiaoming 
        xiaoming.deduce(self.human.id)
        self.assertTrue(xiaoming.is_subset_of(self.primate.id))