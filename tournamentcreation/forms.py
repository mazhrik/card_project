from django.forms import ModelForm
from .models import Tournament, Session


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        # fields = ['title', 'coordinator']
        fields = '__all__'