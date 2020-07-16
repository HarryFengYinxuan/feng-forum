from django import forms

from .models import Notification

class NotificationCreateForm(forms.ModelForm):
    
    
    class Meta:
        model = Notification
        fields = '__all__'


NotificationFormSet = forms.modelformset_factory(Notification, extra=0, 
                                                 fields=('read',))