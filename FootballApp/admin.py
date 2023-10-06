from django.contrib import admin
from .models import User,FootballClub,Player, Like, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(FootballClub)
admin.site.register(Player)
admin.site.register(Like)
admin.site.register(Comment)
