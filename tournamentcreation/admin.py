from django.contrib import admin
from .models import Tournament, Team, TeamPlayer, Session, Segment, Match, TD, Seating, UserProfile, Session_Segments

# Register your models here.
admin.site.register(Tournament)
admin.site.register(Session)
admin.site.register(Session_Segments)
admin.site.register(TeamPlayer)
admin.site.register(Team)
admin.site.register(Match)
# admin.site.register(GlobalTD)
# admin.site.register(LocalTD)
admin.site.register(TD)
admin.site.register(Segment)
admin.site.register(Seating)
admin.site.register(UserProfile)