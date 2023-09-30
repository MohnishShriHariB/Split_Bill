from django.forms import ModelForm,SelectMultiple
from .models import trip,tasks,friend

class Tripform(ModelForm):
    class Meta:
        model = trip
        fields = ['trip_name','trip_completed']


class Taskform(ModelForm):
    class Meta:
        model = tasks
        fields = ['task','whopaid','taskexp']

class Friendform(ModelForm):
    class Meta:
        model=friend
        fields=['friends']
