import uuid

from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class DSet(models.Model):
    ''' A set to deduce information. '''

    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4,
        help_text="Unique ID to query the DObject",
        )
    name = models.CharField(max_length=100, blank=True)
    parents = models.ManyToManyField(
        'DSet',
        help_text='The DSets it is a subset of.',
        blank=True)


    class Meta:
        ordering = ['name']

    
    def deduce(self, parent_id):
        ''' Propagating all parents of this parent to self. Basically subset law.'''

        parent = self.parents.get(id=parent_id)
        # getting all its parents and adding to self
        for grandparent in parent.parents.all():
            self.parents.add(grandparent)

    def is_subset_of(self, parent_id):
        ''' Returns if self is a subset of a certain DSet. '''

        try:
            parent = self.parents.get(id=parent_id)
            return True
        except ObjectDoesNotExist:
            return False

