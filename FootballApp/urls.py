from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("register",views.register,name="register"),
    path("clubs",views.clubs_list,name="clubs_list"),
    path("players",views.players,name="players"),
    path('aboutus',views.aboutus,name="aboutus"),
    path('contactus',views.contactus,name="contactus"),
    path("club/<int:club_id>/",views.club_page,name="club_page"),
    path('club/<int:club_id>/like/',views.like_club,name="like_club"),
    path('submit_club/',views.submit_club,name="submit_club"),
    path('add_player/',views.add_player,name="add_player")
]

