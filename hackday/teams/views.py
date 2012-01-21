from django.views.generic import DetailView, ListView
from teams.models import Team


class TeamList(ListView):
    model = Team
    queryset = Team.objects.order_by('-name')


class TeamDetail(DetailView):
    model = Team
